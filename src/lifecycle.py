# lifecycle_config.py

from minio.lifecycleconfig import Expiration, LifecycleConfig, Rule
from minio.commonconfig import ENABLED, Filter

class lifecycle:
    def __init__(self, prefix: str, expire_day: int):
        self.prefix = prefix
        self.expire_day = expire_day
    
    def get_config(self):
        lifecycle = LifecycleConfig(
                    [
                        Rule(
                            ENABLED,
                            rule_filter=Filter(prefix=self.prefix + '/'),
                            rule_id=self.prefix + '_' + str(self.expire_day),
                            expiration=Expiration(days=self.expire_day),
                        ),
                    ],
                    )
        return lifecycle



