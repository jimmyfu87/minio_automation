## bucket

import datetime
from datetime import timedelta
from typing import List

class Bucket():
    def __init__(self, bucket_name: str, project_name: str,  privacy_ind: str, purpose: str, permission:str, quota: int ) -> None:
        ## Bucket名稱
        self._bucket_name = bucket_name
        ## Project名稱
        self._project_name = project_name
        ## 安全性設定
        self._privacy_ind = privacy_ind
        ## 用途類型
        self._purpose = purpose
        ## 使用權限(RO/RW)
        self._permission = permission
        ## 容量
        self._quota = quota
        ## 建立時間
        # self._create_time = datetime.datetime.now(tzinfo = datetime.timezone(timedelta(hours = 8)))
        ## 使用量
        self._usage = 0
        ## 使用率
        self._use_ratio = 0
        ## 健康狀態
        self._status = 'Healthy'
    
    @property
    def bucket_name(self) -> str:
        return self._bucket_name

    @bucket_name.setter
    def set_bucket_name(self, bucket_name: str) -> None:
        self._bucket_name = bucket_name
    
    @property
    def project_name(self) -> str:
        return self._project_name
    
    @project_name.setter
    def set_project_name(self, project_name: str) -> None:
        self._project_name = project_name

    @property
    def privacy_ind(self) -> str:
        return self._privacy_ind

    @privacy_ind.setter
    def set_privacy_ind(self, privacy_ind: str) -> None:
        self._privacy_ind = privacy_ind

    @property
    def purpose(self) -> str:
        return self._purpose

    @purpose.setter
    def set_purpose(self, purpose: str) -> None:
        self._purpose = purpose

    @property
    def permission(self) -> str:
        return self._permission

    @permission.setter
    def set_permission(self, permission: str) -> None:
        self._permission = permission

    @property
    def quota(self) -> int:
        return self._quota

    @quota.setter
    def set_quota(self, quota: int) -> None:
        self._quota = quota
    
    @property
    def usage(self) -> float:
        return self._usage

    @usage.setter
    def set_usage(self, usage: float) -> None:
        self._usage = usage 

    @property
    def use_ratio(self) -> float:
        return self._use_ratio

    @use_ratio.setter
    def set_use_ratio(self, use_ratio: float) -> None:
        self._use_ratio = use_ratio
    
    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def set_status(self, status: str) -> None:
        self._status = status