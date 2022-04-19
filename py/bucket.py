## bucket

import datetime
from datetime import timedelta
from typing import List

class Bucket():
    def __init__(self, bucket_name: str, project_name: str,  privacy_ind: str, purpose: str, permission:str, team_member_ids: List[str], quota: int ) -> None:
        ## Bucket名稱
        self.bucket_name = bucket_name
        ## Project名稱
        self.project_name = project_name
        ## 安全性設定
        self.privacy_ind = privacy_ind
        ## 用途類型
        self.purpose = purpose
        ## 使用權限(RO/RW)
        self.permission = permission
        ## 容量
        self.quota = quota
        ## 建立時間
        self.create_time = datetime.datetime.now(tzinfo = datetime.timezone(timedelta(hours = 8)))
        ## 使用量
        self.usage = 0
        ## 使用率
        self.use_ratio = 0
        ## 健康狀態
        self.status = 'Healthy'
    
    @property
    def bucket_name(self) -> str:
        return self.project_name

    @property.setter
    def bucket_name(self, bucket_name: str) -> None:
        self.bucket_name = bucket_name
    
    @property
    def project_name(self) -> str:
        return self.project_name
    
    @property.setter
    def project_name(self, project_name: str) -> None:
        self.project_name = project_name

    @property
    def privacy_ind(self) -> str:
        return self.privacy_ind

    @property.setter
    def privacy_ind(self, privacy_ind: str) -> None:
        self.privacy_ind = privacy_ind

    @property
    def purpose(self) -> str:
        return self.purpose

    @property.setter
    def purpose(self, purpose: str) -> None:
        self.purpose = purpose

    @property
    def permission(self) -> str:
        return self.permission

    @property.setter
    def permission(self, permission: str) -> None:
        self.permission = permission

    @property
    def quota(self) -> int:
        return self.quota

    @property.setter
    def quota(self, quota: int) -> None:
        self.quota = quota
    
    @property
    def create_time(self) -> str:
        return self.create_time
    
    @property
    def usage(self) -> float:
        return self.usage

    @property.setter
    def usage(self, usage: float) -> None:
        self.usage = usage 

    @property
    def use_ratio(self) -> float:
        return self.use_ratio

    @property.setter
    def use_ratio(self, use_ratio: float) -> None:
        self.use_ratio = use_ratio
    
    @property
    def status(self) -> str:
        return self.status

    @property.setter
    def status(self, status: str) -> None:
        self.status = status