"""
阴影计算API端点
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from app.services.shadow_service import ShadowService
from app.utils.logger import logger

router = APIRouter()


class ShadowCalculationRequest(BaseModel):
    """阴影计算请求"""
    building_ids: List[int]
    date: str  # YYYY-MM-DD
    hour: int
    minute: int = 0


class ShadowCompareRequest(BaseModel):
    """阴影对比请求"""
    building_id: int
    hour: int = 12  # 默认正午


@router.post("/calculate")
async def calculate_shadows(request: ShadowCalculationRequest):
    """
    计算建筑阴影

    使用Shadow Volume算法计算建筑在指定时间的投影阴影
    """
    try:
        logger.info(
            f"计算阴影: buildings={request.building_ids}, "
            f"time={request.date} {request.hour}:{request.minute}"
        )

        service = ShadowService()

        # 解析日期
        try:
            target_date = datetime.strptime(request.date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="日期格式错误，请使用 YYYY-MM-DD")

        # 计算阴影
        shadows = await service.calculate_shadows(
            building_ids=request.building_ids,
            target_date=target_date,
            hour=request.hour,
            minute=request.minute,
        )

        return {
            "code": 200,
            "data": {
                "shadows": shadows,
                "calculation_time_ms": shadows.get("calculation_time_ms", 0) if isinstance(shadows, dict) else 0,
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"计算阴影失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"计算阴影失败: {str(e)}")


@router.get("/compare-extremes")
async def compare_extreme_shadows(
    building_id: int = Query(..., description="建筑ID"),
    hour: int = Query(12, ge=0, le=23, description="小时（默认正午）"),
):
    """
    对比极端日期的阴影

    对比冬至日（阴影最长）和夏至日（阴影最短）的阴影范围
    """
    try:
        logger.info(f"对比极端阴影: building={building_id}, hour={hour}")

        service = ShadowService()

        # 计算极端日期阴影对比
        comparison = await service.compare_extreme_shadows(
            building_id=building_id,
            hour=hour,
        )

        return {
            "code": 200,
            "data": comparison,
        }

    except Exception as e:
        logger.error(f"对比极端阴影失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"对比极端阴影失败: {str(e)}")


@router.get("/animation")
async def get_shadow_animation(
    building_id: int = Query(..., description="建筑ID"),
    date: str = Query(..., description="日期 YYYY-MM-DD"),
    start_hour: int = Query(6, ge=0, le=23, description="开始小时"),
    end_hour: int = Query(18, ge=0, le=23, description="结束小时"),
    step_minutes: int = Query(15, ge=1, le=60, description="时间步长（分钟）"),
):
    """
    获取阴影动画数据

    返回指定时间段内的多个时刻的阴影数据，用于前端动画播放
    """
    try:
        logger.info(
            f"生成阴影动画: building={building_id}, date={date}, "
            f"time={start_hour}:00-{end_hour}:00, step={step_minutes}min"
        )

        service = ShadowService()

        # 解析日期
        try:
            target_date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="日期格式错误，请使用 YYYY-MM-DD")

        # 生成动画帧
        frames = await service.generate_shadow_animation(
            building_id=building_id,
            target_date=target_date,
            start_hour=start_hour,
            end_hour=end_hour,
            step_minutes=step_minutes,
        )

        return {
            "code": 200,
            "data": {
                "building_id": building_id,
                "date": date,
                "frames": frames,
                "frame_count": len(frames),
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"生成阴影动画失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"生成阴影动画失败: {str(e)}")


@router.delete("/cache")
async def clear_shadow_cache(
    building_id: Optional[int] = Query(None, description="建筑ID，不指定则清空所有"),
):
    """
    清空阴影缓存

    删除缓存的阴影计算结果，下次计算时将重新计算
    """
    try:
        service = ShadowService()
        deleted_count = await service.clear_cache(building_id)

        return {
            "code": 200,
            "data": {
                "deleted_count": deleted_count,
                "message": f"已清空 {deleted_count} 条缓存记录",
            },
        }

    except Exception as e:
        logger.error(f"清空阴影缓存失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"清空阴影缓存失败: {str(e)}")
