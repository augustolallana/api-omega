from typing import List, Optional
import uuid
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Column
from sqlalchemy.dialects.postgresql import JSONB
from typing import Optional
import datetime


# ----- Base class that allows dynamic keys -----
class FlexibleBase(BaseModel):
    class Config:
        extra = 'allow'  # accept unexpected fields


# ----- Theme -----
class ButtonColors(FlexibleBase):
    bg: Optional[str] = None
    text: Optional[str] = None
    hover: Optional[str] = None


class Colors(FlexibleBase):
    primary: Optional[str] = None
    secondary: Optional[str] = None
    background: Optional[str] = None
    text: Optional[str] = None
    button: Optional[ButtonColors] = None


class FontSizes(FlexibleBase):
    small: Optional[str] = None
    medium: Optional[str] = None
    large: Optional[str] = None
    xl: Optional[str] = None


class Fonts(FlexibleBase):
    heading: Optional[str] = None
    body: Optional[str] = None
    sizes: Optional[FontSizes] = None


class Theme(FlexibleBase):
    colors: Optional[Colors] = None
    fonts: Optional[Fonts] = None


# ----- Layout -----
class Spacing(FlexibleBase):
    padding: Optional[str] = None
    margin: Optional[str] = None


class Layout(FlexibleBase):
    containerWidth: Optional[str] = None
    spacing: Optional[Spacing] = None
    borderRadius: Optional[str] = None


# ----- Assets -----
class Assets(FlexibleBase):
    logo: Optional[str] = None
    favicon: Optional[str] = None
    heroImage: Optional[str] = None
    backgroundPattern: Optional[str] = None


# ----- Components -----
class NavbarLink(FlexibleBase):
    label: Optional[str] = None
    href: Optional[str] = None


class Navbar(FlexibleBase):
    fixed: Optional[bool] = None
    style: Optional[str] = None
    links: Optional[List[NavbarLink]] = None


class SocialLink(FlexibleBase):
    platform: Optional[str] = None
    url: Optional[str] = None


class Footer(FlexibleBase):
    columns: Optional[int] = None
    socialLinks: Optional[List[SocialLink]] = None


class Components(FlexibleBase):
    navbar: Optional[Navbar] = None
    footer: Optional[Footer] = None


# ----- SEO -----
class SEO(FlexibleBase):
    title: Optional[str] = None
    description: Optional[str] = None
    keywords: Optional[List[str]] = None


# ----- Root Schema -----
class ConfigSchema(FlexibleBase):
    theme: Optional[Theme] = None
    layout: Optional[Layout] = None
    assets: Optional[Assets] = None
    components: Optional[Components] = None
    seo: Optional[SEO] = None


class Config(SQLModel, table=True):
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True
    )

    # Store config as JSON (use JSONB for Postgres)
    data: dict = Field(sa_column=Column(JSONB))

    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
