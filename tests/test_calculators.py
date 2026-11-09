from decimal import Decimal

import pytest
from pydantic import ValidationError

from vissotia_assistant.calculators import (
    RenovateAndSellInput,
    RentalSimulationInput,
    simulate_renovate_and_sell,
    simulate_rental_investment,
)


def test_rental_case_matches_approved_corpus() -> None:
    result = simulate_rental_investment(
        RentalSimulationInput(
            purchase_price=180_000,
            acquisition_costs=18_000,
            renovation_costs=12_000,
            other_initial_costs=2_000,
            monthly_rent=1_100,
            occupied_months_per_year=11,
            annual_operating_costs=2_400,
            annual_financing_costs=3_600,
        )
    )

    assert result.total_initial_investment == Decimal("212000.00")
    assert result.annual_gross_income == Decimal("12100.00")
    assert result.annual_net_income_before_financing == Decimal("9700.00")
    assert result.annual_cash_flow_after_financing == Decimal("6100.00")
    assert result.gross_yield_pct == Decimal("5.71")
    assert result.net_yield_before_financing_pct == Decimal("4.58")
    assert result.label == "Simulación orientativa"


def test_rental_allows_negative_cash_flow() -> None:
    result = simulate_rental_investment(
        RentalSimulationInput(
            purchase_price=100_000,
            acquisition_costs=0,
            renovation_costs=0,
            other_initial_costs=0,
            monthly_rent=500,
            occupied_months_per_year=10,
            annual_operating_costs=3_000,
            annual_financing_costs=4_000,
        )
    )
    assert result.annual_cash_flow_after_financing == Decimal("-2000.00")


def test_rental_rejects_zero_total_investment() -> None:
    data = RentalSimulationInput(
        purchase_price=0,
        acquisition_costs=0,
        renovation_costs=0,
        other_initial_costs=0,
        monthly_rent=500,
        occupied_months_per_year=12,
        annual_operating_costs=0,
    )
    with pytest.raises(ValueError, match="mayor que cero"):
        simulate_rental_investment(data)


def test_rental_rejects_more_than_twelve_months() -> None:
    with pytest.raises(ValidationError):
        RentalSimulationInput(
            purchase_price=100_000,
            acquisition_costs=0,
            renovation_costs=0,
            other_initial_costs=0,
            monthly_rent=500,
            occupied_months_per_year=13,
            annual_operating_costs=0,
        )


def test_rental_rejects_negative_values() -> None:
    with pytest.raises(ValidationError):
        RentalSimulationInput(
            purchase_price=-1,
            acquisition_costs=0,
            renovation_costs=0,
            other_initial_costs=0,
            monthly_rent=500,
            occupied_months_per_year=12,
            annual_operating_costs=0,
        )


def test_flip_case_matches_approved_corpus() -> None:
    result = simulate_renovate_and_sell(
        RenovateAndSellInput(
            purchase_price=145_000,
            acquisition_costs=15_000,
            renovation_budget=40_000,
            renovation_contingency=6_000,
            holding_costs=4_000,
            financing_costs=5_000,
            selling_costs=8_000,
            other_costs=2_000,
            estimated_sale_price=255_000,
        )
    )

    assert result.total_project_cost == Decimal("225000.00")
    assert result.orientative_result == Decimal("30000.00")
    assert result.margin_on_sale_pct == Decimal("11.76")
    assert result.return_on_total_cost_pct == Decimal("13.33")


def test_flip_allows_negative_result() -> None:
    result = simulate_renovate_and_sell(
        RenovateAndSellInput(
            purchase_price=100_000,
            acquisition_costs=10_000,
            renovation_budget=30_000,
            renovation_contingency=5_000,
            holding_costs=3_000,
            financing_costs=2_000,
            selling_costs=5_000,
            other_costs=0,
            estimated_sale_price=140_000,
        )
    )
    assert result.orientative_result == Decimal("-15000.00")
    assert result.return_on_total_cost_pct < 0


def test_flip_rejects_zero_sale_price() -> None:
    with pytest.raises(ValidationError):
        RenovateAndSellInput(
            purchase_price=100_000,
            acquisition_costs=0,
            renovation_budget=0,
            renovation_contingency=0,
            holding_costs=0,
            financing_costs=0,
            selling_costs=0,
            other_costs=0,
            estimated_sale_price=0,
        )


def test_models_reject_unexpected_fields() -> None:
    with pytest.raises(ValidationError):
        RentalSimulationInput(
            purchase_price=100_000,
            acquisition_costs=0,
            renovation_costs=0,
            other_initial_costs=0,
            monthly_rent=500,
            occupied_months_per_year=12,
            annual_operating_costs=0,
            address="dato no permitido",
        )
