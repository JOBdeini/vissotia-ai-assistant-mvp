"""Cálculos deterministas para las simulaciones orientativas del MVP."""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator

MONEY_PLACES = Decimal("0.01")
PERCENT_PLACES = Decimal("0.01")
DISCLAIMER = (
    "Este ejemplo no constituye una valoración, previsión ni recomendación de inversión. "
    "Verifica los datos y consulta a profesionales cualificados antes de tomar una decisión real."
)


def _money(value: Decimal) -> Decimal:
    return value.quantize(MONEY_PLACES, rounding=ROUND_HALF_UP)


def _percent(value: Decimal) -> Decimal:
    return value.quantize(PERCENT_PLACES, rounding=ROUND_HALF_UP)


class NonNegativeMoneyModel(BaseModel):
    """Base estricta para impedir importes negativos o valores no declarados."""

    model_config = ConfigDict(extra="forbid")

    @field_validator("*", mode="before")
    @classmethod
    def reject_booleans(cls, value: object) -> object:
        if isinstance(value, bool):
            raise ValueError("Los campos numéricos no aceptan valores booleanos.")
        return value


class RentalSimulationInput(NonNegativeMoneyModel):
    purchase_price: Decimal = Field(ge=0)
    acquisition_costs: Decimal = Field(ge=0)
    renovation_costs: Decimal = Field(ge=0)
    other_initial_costs: Decimal = Field(ge=0)
    monthly_rent: Decimal = Field(ge=0)
    occupied_months_per_year: Decimal = Field(ge=0, le=12)
    annual_operating_costs: Decimal = Field(ge=0)
    annual_financing_costs: Decimal = Field(default=Decimal("0"), ge=0)


class RentalSimulationResult(BaseModel):
    label: str = "Simulación orientativa"
    total_initial_investment: Decimal
    annual_gross_income: Decimal
    annual_net_income_before_financing: Decimal
    annual_cash_flow_after_financing: Decimal
    gross_yield_pct: Decimal
    net_yield_before_financing_pct: Decimal
    disclaimer: str = DISCLAIMER


def simulate_rental_investment(data: RentalSimulationInput) -> RentalSimulationResult:
    """Calcula una simulación de alquiler usando únicamente los datos recibidos."""

    total = (
        data.purchase_price
        + data.acquisition_costs
        + data.renovation_costs
        + data.other_initial_costs
    )
    if total <= 0:
        raise ValueError("La inversión inicial total debe ser mayor que cero.")

    gross_income = data.monthly_rent * data.occupied_months_per_year
    net_income = gross_income - data.annual_operating_costs
    cash_flow = net_income - data.annual_financing_costs

    return RentalSimulationResult(
        total_initial_investment=_money(total),
        annual_gross_income=_money(gross_income),
        annual_net_income_before_financing=_money(net_income),
        annual_cash_flow_after_financing=_money(cash_flow),
        gross_yield_pct=_percent(gross_income / total * 100),
        net_yield_before_financing_pct=_percent(net_income / total * 100),
    )


class RenovateAndSellInput(NonNegativeMoneyModel):
    purchase_price: Decimal = Field(ge=0)
    acquisition_costs: Decimal = Field(ge=0)
    renovation_budget: Decimal = Field(ge=0)
    renovation_contingency: Decimal = Field(ge=0)
    holding_costs: Decimal = Field(ge=0)
    financing_costs: Decimal = Field(ge=0)
    selling_costs: Decimal = Field(ge=0)
    other_costs: Decimal = Field(ge=0)
    estimated_sale_price: Decimal = Field(gt=0)


class RenovateAndSellResult(BaseModel):
    label: str = "Simulación orientativa"
    total_project_cost: Decimal
    estimated_sale_price: Decimal
    orientative_result: Decimal
    margin_on_sale_pct: Decimal
    return_on_total_cost_pct: Decimal
    disclaimer: str = DISCLAIMER


def simulate_renovate_and_sell(data: RenovateAndSellInput) -> RenovateAndSellResult:
    """Calcula una simulación de compra, reforma y venta."""

    total = (
        data.purchase_price
        + data.acquisition_costs
        + data.renovation_budget
        + data.renovation_contingency
        + data.holding_costs
        + data.financing_costs
        + data.selling_costs
        + data.other_costs
    )
    if total <= 0:
        raise ValueError("El coste total del proyecto debe ser mayor que cero.")

    result = data.estimated_sale_price - total

    return RenovateAndSellResult(
        total_project_cost=_money(total),
        estimated_sale_price=_money(data.estimated_sale_price),
        orientative_result=_money(result),
        margin_on_sale_pct=_percent(result / data.estimated_sale_price * 100),
        return_on_total_cost_pct=_percent(result / total * 100),
    )
