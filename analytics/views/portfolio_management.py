from http import HTTPMethod

import pandas as pd
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from core.metadata.openapi import OpenApiTags
from core.renderer import CustomRenderer
from db import engine

from ..models import DailyNetFundFlow, TradeVsClient
from ..orm import (
    DailyNetFundFlowOrm,
    TurnoverAndClientsTradeOrm,
    TurnoverPerformanceOrm,
)

__all__ = [
    "get_daily_net_fundflow",
    "get_daily_net_fundflow_by_branchid",
    "get_trade_vs_client_statistics",
    "get_trade_vs_client_statistics_by_branchid",
    "get_turnover_performance",
    "get_turnover_performance_by_branchid",
]


@extend_schema(tags=[OpenApiTags.PM])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_daily_net_fundflow(request: Request) -> Response:
    """fetch basic branch summary"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = select(
            DailyNetFundFlowOrm.trading_date.label("trading_date"),
            func.sum(DailyNetFundFlowOrm.fundflow).label("amount"),
        ).group_by(DailyNetFundFlowOrm.trading_date)

        rows = session.execute(qs)
        results = [
            DailyNetFundFlow.model_validate(row._asdict()).model_dump() for row in rows
        ]
    return Response(results)


@extend_schema(tags=[OpenApiTags.PM])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_daily_net_fundflow_by_branchid(request: Request, id: int) -> Response:
    """fetch basic branch summary"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = (
            select(
                DailyNetFundFlowOrm.trading_date.label("trading_date"),
                func.sum(DailyNetFundFlowOrm.fundflow).label("amount"),
            )
            .where(DailyNetFundFlowOrm.branch_code == id)
            .group_by(DailyNetFundFlowOrm.trading_date)
        )

        rows = session.execute(qs)
        results = [
            DailyNetFundFlow.model_validate(row._asdict()).model_dump() for row in rows
        ]
    return Response(results)


@extend_schema(tags=[OpenApiTags.PM])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_trade_vs_client_statistics(request: Request) -> Response:
    """fetch basic branch summary"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = select(
            TurnoverAndClientsTradeOrm.trading_date.label("trading_date"),
            func.sum(TurnoverAndClientsTradeOrm.turnover).label("turnover"),
            func.sum(TurnoverAndClientsTradeOrm.active_client).label("active_clients"),
        ).group_by(TurnoverAndClientsTradeOrm.trading_date)

        rows = session.execute(qs)
        results = [
            TradeVsClient.model_validate(row._asdict()).model_dump() for row in rows
        ]
    return Response(results)


@extend_schema(tags=[OpenApiTags.PM])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_trade_vs_client_statistics_by_branchid(request: Request, id: int) -> Response:
    """fetch basic branch summary"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = (
            select(
                TurnoverAndClientsTradeOrm.trading_date.label("trading_date"),
                func.sum(TurnoverAndClientsTradeOrm.turnover).label("turnover"),
                func.sum(TurnoverAndClientsTradeOrm.active_client).label(
                    "active_clients"
                ),
            )
            .where(TurnoverAndClientsTradeOrm.branch_code == id)
            .group_by(TurnoverAndClientsTradeOrm.trading_date)
        )

        rows = session.execute(qs)
        results = [
            TradeVsClient.model_validate(row._asdict()).model_dump() for row in rows
        ]
    return Response(results)


@extend_schema(tags=[OpenApiTags.PM])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_turnover_performance(request: Request) -> Response:
    """fetch summary of turnover performance"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        query = select(
            TurnoverPerformanceOrm.branch_code,
            TurnoverPerformanceOrm.branch_name,
            TurnoverPerformanceOrm.col1,
            TurnoverPerformanceOrm.col2,
            TurnoverPerformanceOrm.col3,
        )
        rows = session.execute(query)

        df = pd.DataFrame([row._asdict() for row in rows], columns=rows.keys())
        df["col2"] = df["col2"].str.strip()  # trim the col2, has space

        pivot_df = df.pivot_table(
            index="col2", columns="col3", values="col1", aggfunc="sum"
        ).reset_index()  # aggregate the df

        pivot_df.columns = map(str.lower, pivot_df.columns)

        pivot_df.rename(columns={"col2": "name"}, inplace=True)
    return Response(pivot_df.to_dict(orient="records"))


@extend_schema(tags=[OpenApiTags.PM])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_turnover_performance_by_branchid(request: Request, id: int) -> Response:
    """fetch summary of turnover performance"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        query = select(
            TurnoverPerformanceOrm.branch_code,
            TurnoverPerformanceOrm.branch_name,
            TurnoverPerformanceOrm.col1,
            TurnoverPerformanceOrm.col2,
            TurnoverPerformanceOrm.col3,
        ).where(TurnoverPerformanceOrm.branch_code == id)
        rows = session.execute(query)

        df = pd.DataFrame([row._asdict() for row in rows], columns=rows.keys())
        df["col2"] = df["col2"].str.strip()  # trim the col2, has space

        pivot_df = df.pivot_table(
            index="col2", columns="col3", values="col1", aggfunc="sum"
        ).reset_index()  # aggregate the df

        pivot_df.columns = map(str.lower, pivot_df.columns)

        pivot_df.rename(
            columns={
                "col2": "name",
            },
            inplace=True,
        )
    return Response(pivot_df.to_dict(orient="records"))