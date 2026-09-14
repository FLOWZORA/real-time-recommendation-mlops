from feast import FeatureView, Field, Entity
from feast.types import Int64
from feast.infra.offline_stores.file_source import FileSource
from datetime import timedelta
from pathlib import Path

user_entity = Entity(name="user_id", join_keys=["user_id"])
item_entity = Entity(name="item_id", join_keys=["item_id"])

data_path = Path(__file__).resolve().parent.parent / "feature_store" / "data" / "user_features.parquet"

user_item_features = FeatureView(
    name="user_item_features",
    entities=[user_entity, item_entity],
    ttl=timedelta(days=1),
    schema=[
        Field(name="views", dtype=Int64),
        Field(name="clicks", dtype=Int64),
        Field(name="purchases", dtype=Int64),
    ],
    source=FileSource(
        path=data_path.as_posix(),
        timestamp_field="event_timestamp",
    ),
)

