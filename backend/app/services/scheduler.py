# backend/app/services/scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.services.arbitrage_engine import ArbitrageEngine
from app.services.strategy_runner import StrategyRunner
from app.db.session import SessionLocal
from loguru import logger


def run_arbitrage_task():
    logger.info("⏱️ [TAREA] Ejecutando arbitraje programado...")
    db = SessionLocal()
    try:
        engine = ArbitrageEngine(db=db)
        engine.run()
    finally:
        db.close()


def run_trading_task():
    logger.info("⏱️ [TAREA] Ejecutando estrategias de trading...")
    db = SessionLocal()
    try:
        runner = StrategyRunner(db_session=db)
        runner.execute_strategies()
    finally:
        db.close()


def start_scheduler():
    scheduler = BackgroundScheduler()
    logger.info("🧠 Iniciando scheduler...")

    # Ejecutar arbitraje cada 60 segundos
    scheduler.add_job(
        run_arbitrage_task,
        trigger=IntervalTrigger(seconds=60),
        id="arbitrage_task",
        replace_existing=True
    )

    # Ejecutar trading cada 30 segundos
    scheduler.add_job(
        run_trading_task,
        trigger=IntervalTrigger(seconds=30),
        id="trading_task",
        replace_existing=True
    )

    scheduler.start()
    logger.success("✅ Scheduler iniciado.")
    return scheduler
