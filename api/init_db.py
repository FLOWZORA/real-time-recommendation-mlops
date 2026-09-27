import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from sqlalchemy.orm import Session
from api.database import engine, SessionLocal, Base
import api.models  # Ensures all models are registered on Base
from api.models.organization import Organization, OrganizationMember
from api.models.user import User
from api.models.product import Category, Product
from api.models.experiment import Experiment
from api.models.api_key import ApiKey
from api.security.auth import get_password_hash
from api.security.api_keys import hash_api_key
from features.catalog_data import CATEGORIES, get_item_metadata

DEMO_API_KEY_SECRET = "reco_live_demo123456789abcdef01234567"

def init_db():
    print("[INFO] Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    print("[OK] Database tables created successfully.")

    db: Session = SessionLocal()
    try:
        # 1. Seed Demo Organization
        org = db.query(Organization).filter(Organization.slug == "demo-store").first()
        if not org:
            org = Organization(
                name="RecommendationOS Demo Store",
                slug="demo-store",
                plan="enterprise",
            )
            db.add(org)
            db.flush()
            print(f"[OK] Seeded demo organization: {org.name} ({org.id})")

        # 2. Seed Default Users
        users_seed = [
            ("admin@recommendationos.io", "AdminPassword123!", "Admin User", "STORE_ADMIN"),
            ("mlops@recommendationos.io", "MLOpsPassword123!", "ML Engineer", "ML_ENGINEER"),
            ("customer@example.com", "CustomerPassword123!", "Alex Chen", "CUSTOMER"),
        ]

        for email, pwd, name, role in users_seed:
            existing = db.query(User).filter(User.email == email).first()
            if not existing:
                u = User(
                    email=email,
                    hashed_password=get_password_hash(pwd),
                    full_name=name,
                    role=role,
                )
                db.add(u)
                db.flush()
                # Add membership
                m = OrganizationMember(
                    organization_id=org.id,
                    user_id=u.id,
                    role=role,
                )
                db.add(m)
                print(f"[OK] Seeded user {email} ({role})")

        # 3. Seed Categories
        category_map = {}
        for cat_info in CATEGORIES:
            cat_name = cat_info["name"]
            slug = cat_name.lower().replace(" & ", "-").replace(" ", "-")
            existing_cat = db.query(Category).filter(
                Category.organization_id == org.id,
                Category.slug == slug,
            ).first()
            if not existing_cat:
                cat = Category(
                    organization_id=org.id,
                    name=cat_name,
                    slug=slug,
                    icon=cat_info.get("icon", "📦"),
                    color=cat_info.get("color", "#6366f1"),
                )
                db.add(cat)
                db.flush()
                category_map[cat_name] = cat.id
            else:
                category_map[cat_name] = existing_cat.id

        # 4. Seed 500 Products mapped to vector index (0..499)
        existing_count = db.query(Product).filter(Product.organization_id == org.id).count()
        if existing_count < 500:
            print(f"[INFO] Seeding catalog products (current count: {existing_count})...")
            for item_idx in range(500):
                meta = get_item_metadata(item_idx)
                existing_p = db.query(Product).filter(
                    Product.organization_id == org.id,
                    Product.item_id_numeric == item_idx,
                ).first()
                if not existing_p:
                    cat_id = category_map.get(meta.get("category"))
                    p = Product(
                        organization_id=org.id,
                        item_id_numeric=item_idx,
                        category_id=cat_id,
                        title=meta.get("title", f"Product {item_idx}"),
                        description=f"High-performance {meta.get('category', 'Hardware')} designed for modern workflows.",
                        price=float(meta.get("price", 99.99)),
                        rating=float(meta.get("rating", 4.8)),
                        reviews_count=int(meta.get("reviews", 100)),
                        badge=meta.get("badge", "Popular"),
                        image_url=f"https://picsum.photos/seed/{item_idx}/400/300",
                        in_stock=True,
                        popularity_score=max(0, 500 - item_idx),
                    )
                    db.add(p)
            db.flush()
            print(f"[OK] Seeded 500 catalog items into PostgreSQL/SQLite database.")

        # 5. Seed Demo API Key
        hashed_demo_key = hash_api_key(DEMO_API_KEY_SECRET)
        existing_key = db.query(ApiKey).filter(ApiKey.hashed_key == hashed_demo_key).first()
        if not existing_key:
            demo_key = ApiKey(
                organization_id=org.id,
                name="Default Production Store Key",
                key_prefix=DEMO_API_KEY_SECRET[:12],
                hashed_key=hashed_demo_key,
                scopes=["read:recommendations", "write:events", "read:products"],
            )
            db.add(demo_key)
            print(f"[OK] Seeded Demo API Key: {DEMO_API_KEY_SECRET}")

        # 6. Seed Default A/B Experiment
        exp = db.query(Experiment).filter(
            Experiment.organization_id == org.id,
            Experiment.name == "TwoTower-v1-vs-v2",
        ).first()
        if not exp:
            exp = Experiment(
                organization_id=org.id,
                name="TwoTower-v1-vs-v2",
                status="ACTIVE",
                variant_a_model="TwoTowerRecommender:Production",
                variant_b_model="TwoTowerRecommender:Staging",
                traffic_split_b=0.2,
            )
            db.add(exp)
            print("[OK] Seeded active A/B experiment: TwoTower-v1-vs-v2 (80/20 split)")

        db.commit()
        print("[SUCCESS] Database initialization and seed complete!")
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Database initialization failed: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
