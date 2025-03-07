from datetime import datetime

from sqlalchemy import DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from db import BaseOrm

__all__ = [
    "RMWiseOverallSummaryOrm",
    "RMWiseDailyTurnoverPerformanceOrm",
    "RMWiseSectorExposureCashCodeOrm",
    "RMWiseSectorExposureMarginCodeOrm",
    "RMWiseEcrmDetailsOrm",
    "RMWiseDailyTradeDataOrm",
]


class RMWiseOverallSummaryOrm(BaseOrm):
    __tablename__ = "BI_trd_RMWise_Client_Cash_Margin_Details"

    rm_id: Mapped[str] = mapped_column("RM_id", String(50), primary_key=True)
    rm_name: Mapped[str] = mapped_column("RM_Name", String(255))
    branch_code: Mapped[int] = mapped_column("branch_Code", Integer, primary_key=True)
    total_client: Mapped[float] = mapped_column("Total_client", Integer, nullable=False)
    total_active_client: Mapped[float] = mapped_column(
        "Total_Active_client", Integer, nullable=False
    )
    cash_active_client: Mapped[float] = mapped_column(
        "Cash_active_client", Integer, nullable=False
    )
    margin_active_client: Mapped[float] = mapped_column(
        "Margin_active_client", Integer, nullable=False
    )
    cash_balance: Mapped[float] = mapped_column(
        "Cash_balance", Numeric(1), nullable=True
    )
    cash_stock_balance: Mapped[float] = mapped_column(
        "Cash_Stock_balance", Numeric(1), nullable=False
    )
    cash_daily_turnover: Mapped[float] = mapped_column(
        "Cash_Daily_TurnOver", Numeric(1), nullable=False
    )
    margin_balance: Mapped[float] = mapped_column(
        "Margin_balance", Numeric(1), nullable=True
    )
    margin_stock_balance: Mapped[float] = mapped_column(
        "Margin_Stock_balance", Numeric(1), nullable=False
    )
    margin_daily_turnover: Mapped[float] = mapped_column(
        "Margin_Daily_TurnOver", Numeric(1), nullable=False
    )
    daily_turnover: Mapped[float] = mapped_column(
        "Daily_TurnOver", Numeric(1), nullable=False
    )
    net_buy_sell: Mapped[float] = mapped_column(
        "Net_buy_sell", Numeric(1), nullable=False
    )


class RMWiseDailyTurnoverPerformanceOrm(BaseOrm):
    __tablename__ = "BI_trd_RMWise_Daily_TurnOver_TrunOverTarget"

    rm_id: Mapped[str] = mapped_column("RM_id", String(50), primary_key=True)
    rm_name: Mapped[str] = mapped_column("RM_Name", String(255))
    branch_code: Mapped[int] = mapped_column("branch_Code", Integer, primary_key=True)
    trading_date: Mapped[datetime] = mapped_column("trd_Dt", DateTime)
    generated: Mapped[float] = mapped_column("Daily_Turnover_generated", Numeric(1))
    target: Mapped[float] = mapped_column("Daily_Turnover_target", Numeric(1))


class RMWiseSectorExposureCashCodeOrm(BaseOrm):
    __tablename__ = "BI_trd_RMWise_Sector_Exposure_Cash_Codes"

    rm_id: Mapped[str] = mapped_column("RM_id", String(50), primary_key=True)
    rm_name: Mapped[str] = mapped_column("RM_Name", String(255))
    branch_code: Mapped[int] = mapped_column("branch_Code", Integer, primary_key=True)
    total_qty: Mapped[float] = mapped_column(
        "Cash_total_qty", Numeric(1), nullable=False
    )
    sector_name: Mapped[str] = mapped_column(
        "Sector_name", String(50), nullable=False, primary_key=True
    )


class RMWiseSectorExposureMarginCodeOrm(BaseOrm):
    __tablename__ = "BI_trd_RMWise_Sector_Exposure_Margin_Codes"

    rm_id: Mapped[str] = mapped_column("RM_id", String(50), primary_key=True)
    rm_name: Mapped[str] = mapped_column("RM_Name", String(255))
    branch_code: Mapped[int] = mapped_column("branch_Code", Integer, primary_key=True)
    total_qty: Mapped[float] = mapped_column(
        "Cash_total_qty", Numeric(1), nullable=False
    )
    sector_name: Mapped[str] = mapped_column(
        "Sector_name", String(50), nullable=False, primary_key=True
    )


class RMWiseEcrmDetailsOrm(BaseOrm):
    __tablename__ = "BI_trd_RMWise_eCRM_Details"

    rm_name: Mapped[str] = mapped_column("RM_NAME", String(250), primary_key=True)
    region: Mapped[str] = mapped_column("Region", String(50))  
    cluster: Mapped[str] = mapped_column("Cluster", String(20))  
    branch: Mapped[str] = mapped_column("Branch", String(50))  
    branch_code: Mapped[float] = mapped_column("Branch_code", Numeric(3, 0),primary_key=True) 
    total_Visits: Mapped[int] = mapped_column("Total_Visits", Integer)  
    success: Mapped[int] = mapped_column("Success", Integer) 
    inProgress: Mapped[int] = mapped_column("InProgress", Integer)  
    discard: Mapped[int] = mapped_column("Discard", Integer)  
    existingClientVisit: Mapped[int] = mapped_column("ExistingClientVisit", Integer)


class RMWiseDailyTradeDataOrm(BaseOrm):
    __tablename__ = "BI_trd_RMWise_Daily_trade_data"

    push_date: Mapped[DateTime]=mapped_column("Push_date",DateTime)
    branch_code: Mapped[float] = mapped_column("branch_code", Numeric(3, 0),primary_key=True) 
    branch: Mapped[str] = mapped_column("branch_Name", String(50))  
    rm_name: Mapped[str] = mapped_column("RM_Name", String(250), primary_key=True)
    total_client_today: Mapped[int] = mapped_column("total_client_today", Integer) 
    total_turnover_today: Mapped[float] = mapped_column("total_turnover_today", Numeric(38, 5)) 



