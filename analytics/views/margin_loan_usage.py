from enum import StrEnum
from http import HTTPMethod
from typing import Type

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from core.metadata.openapi import OpenApiTags
from core.renderer import CustomRenderer
from db import engine

from ..models import Exposure, MarginLoanUsgae, MarkedInvestor, RMWiseNetTrade
from ..orm import (
    ExposureControllingManagementOrm,
    MarginLoanAllocationUsageOrm,
    NegativeEquityInvestorOrm,
    RedZoneInvestorOrm,
    RMWiseNetTradeOrm,
    YellowZoneInvestorOrm,
)

__all__ = [
    "get_margin_loan_allocations",
    "get_margin_loan_allocations_by_branchid",
    "get_exposures_list",
    "get_exposures_list_by_branchid",
    "get_rmwise_net_trades",
    "get_zone_marked_clients",
]


class MarkedInvestorEnum(StrEnum):
    RED = "red"
    YELLOW = "yellow"
    NEGATIVE_EQUITY = "negative_equity"


InvestorOrmType = RedZoneInvestorOrm | YellowZoneInvestorOrm | NegativeEquityInvestorOrm


def get_marked_investors(
    investor_cls: Type[InvestorOrmType], branch_code: int | None = None
):
    qs = select(
        investor_cls.branch_code,
        func.trim(investor_cls.investor_code).label(
            "investor_code"
        ),  # db has whitespace in values
        func.trim(investor_cls.investor_name).label(
            "investor_name"
        ),  # db has whitespace in values
        investor_cls.ledger_balance,
        investor_cls.rm_name,
    ).order_by(investor_cls.investor_name)
    if branch_code:
        qs = qs.where(investor_cls.branch_code == branch_code)
    return qs


@extend_schema(tags=[OpenApiTags.MLU])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_margin_loan_allocations(request: Request) -> Response:
    """fetch all margin loan allocation summary"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = (
            select(
                MarginLoanAllocationUsageOrm.col2.label("perticular"),
                func.sum(MarginLoanAllocationUsageOrm.col1).label("amount"),
            )
            .group_by(MarginLoanAllocationUsageOrm.col2)
            .order_by(MarginLoanAllocationUsageOrm.col2)
        )
        rows = session.execute(qs)
        results = [
            MarginLoanUsgae.model_validate(row._asdict()).model_dump() for row in rows
        ]
    return Response(results)


@extend_schema(tags=[OpenApiTags.MLU])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_margin_loan_allocations_by_branchid(request: Request, id: int) -> Response:
    """fetch all margin loan allocation summary by brnach id"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = (
            select(
                MarginLoanAllocationUsageOrm.col2.label("perticular"),
                func.sum(MarginLoanAllocationUsageOrm.col1).label("amount"),
            )
            .where(MarginLoanAllocationUsageOrm.branch_code == id)
            .group_by(MarginLoanAllocationUsageOrm.col2)
            .order_by(MarginLoanAllocationUsageOrm.col2)
        )
        rows = session.execute(qs)
        results = [
            MarginLoanUsgae.model_validate(row._asdict()).model_dump() for row in rows
        ]
    return Response(results)


@extend_schema(tags=[OpenApiTags.MLU])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_exposures_list(request: Request) -> Response:
    """fetch all margin loan allocation summary"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = (
            select(
                ExposureControllingManagementOrm.exposure_type.label("exposure"),
                func.sum(ExposureControllingManagementOrm.investors_count).label(
                    "investors"
                ),
                func.sum(ExposureControllingManagementOrm.loan_amount).label(
                    "loan_amount"
                ),
            )
            .group_by(ExposureControllingManagementOrm.exposure_type)
            .order_by(ExposureControllingManagementOrm.exposure_type)
        )
        rows = session.execute(qs)
        results = [Exposure.model_validate(row._asdict()).model_dump() for row in rows]
    return Response(results)


@extend_schema(tags=[OpenApiTags.MLU])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_exposures_list_by_branchid(request: Request, id: int) -> Response:
    """fetch all margin loan allocation summary"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = (
            select(
                ExposureControllingManagementOrm.exposure_type.label("exposure"),
                func.sum(ExposureControllingManagementOrm.investors_count).label(
                    "investors"
                ),
                func.sum(ExposureControllingManagementOrm.loan_amount).label(
                    "loan_amount"
                ),
            )
            .where(ExposureControllingManagementOrm.branch_code == id)
            .group_by(ExposureControllingManagementOrm.exposure_type)
            .order_by(ExposureControllingManagementOrm.exposure_type)
        )
        rows = session.execute(qs)
        results = [Exposure.model_validate(row._asdict()).model_dump() for row in rows]
    return Response(results)


@extend_schema(tags=[OpenApiTags.MLU])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_rmwise_net_trades(request: Request) -> Response:
    """fetch all RM list with net trades"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = select(
            RMWiseNetTradeOrm.branch_code,
            RMWiseNetTradeOrm.branch_name,
            RMWiseNetTradeOrm.investor_code,
            RMWiseNetTradeOrm.opening_balance,
            RMWiseNetTradeOrm.ending_balance,
            RMWiseNetTradeOrm.net_buysell,
            RMWiseNetTradeOrm.rm_name,
        ).order_by(RMWiseNetTradeOrm.branch_name)
        rows = session.execute(qs)
        results = [
            RMWiseNetTrade.model_validate(row._asdict()).model_dump() for row in rows
        ]
    return Response(results)


@extend_schema(
    tags=[OpenApiTags.MLU],
    parameters=[
        OpenApiParameter(
            "investor_type",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            required=True,
            description="Type of the Investors to get",
            enum=MarkedInvestorEnum,
            allow_blank=False,
        ),
        OpenApiParameter(
            "branch_code",
            OpenApiTypes.INT,
            OpenApiParameter.QUERY,
            required=False,
            description="marked investors under specific branch",
        ),
    ],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_zone_marked_clients(request: Request) -> Response:
    """fetch all RM list with net trades"""
    request.accepted_renderer = CustomRenderer()

    mark = request.query_params.get("investor_type")
    branch_code = request.query_params.get("branch_code")

    with Session(engine) as session:
        match mark:
            case MarkedInvestorEnum.RED:
                qs = get_marked_investors(RedZoneInvestorOrm, branch_code)
            case MarkedInvestorEnum.YELLOW:
                qs = get_marked_investors(YellowZoneInvestorOrm, branch_code)
            case _:
                qs = get_marked_investors(NegativeEquityInvestorOrm, branch_code)

        rows = session.execute(qs)
        results = [
            MarkedInvestor.model_validate(row._asdict()).model_dump() for row in rows
        ]
    return Response(results)
