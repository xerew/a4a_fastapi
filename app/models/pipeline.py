from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.config import Base
from app.auth.dependencies import login_required

@router.get("/pipeline-builder", response_class=HTMLResponse)
def pipeline_builder(request: Request):
    user = login_required(request)
    if isinstance(user, RedirectResponse):
        return user  # redirects to /login

    return templates.TemplateResponse("pipeline/builder.html", {"request": request, "user": user})

class Pipeline(Base):
    __tablename__ = "pipelines"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # From cookie
    name = Column(String(255), nullable=False)
    data = Column(Text, nullable=False)  # Will store JSON string
