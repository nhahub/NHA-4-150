# VisualForge AI

VisualForge AI is a full-stack AI visual content studio for text-to-image, image-to-image, inpainting/editing, analytics, gallery history, and a prepared chatbot assistant.

The web app integrates the prepared `visualforge_engine.py` inference engine from `visualforge_web_ready_ai_backend.zip`. It does not retrain, redesign, or add training code for the AI model.

## Features

- Professional dark AI dashboard with Bento Grid layout
- Text-to-Image generation
- Image-to-Image generation
- Inpainting / editing with source and mask uploads
- Domain generation: General / Base, Product Ads, Egyptian Cultural
- Dashboard analytics from PostgreSQL
- Gallery / History with search, filters, details modal, and downloads
- Prepared VisualForge Assistant chatbot module
- FastAPI backend with SQLAlchemy, Alembic, Pydantic schemas, and static image serving
- PostgreSQL database via Docker Compose
- Logo branding with `Logo.png` and `Logo2.png`

## Tech Stack

Frontend:

- React + Vite
- Tailwind CSS
- lucide-react
- Recharts
- Axios

Backend:

- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Pydantic
- Uvicorn
- python-multipart

AI:

- Existing `visualforge_engine.py`
- SDXL inference through the provided engine
- Lazy model loading when generation is requested

## Folder Structure

```text
visualforge-ai/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── features/
│   │   ├── routes/
│   │   └── services/
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── backend/
│   ├── app/
│   │   ├── ai/
│   │   ├── core/
│   │   ├── database/
│   │   ├── modules/
│   │   └── storage/
│   ├── alembic/
│   ├── alembic.ini
│   ├── requirements.txt
│   └── .env.example
├── docker-compose.yml
├── README.md
└── visualforge_web_ready_ai_backend.zip
```

## Run PostgreSQL

From the `visualforge-ai` folder:

```bash
docker compose up -d postgres
```

The database uses:

```text
database: visualforge_db
user: visualforge_user
password: visualforge_password
port: 5432
```

## Run Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend environment example:

```bash
copy .env.example .env
```

Set LoRA paths in `.env` before using `product_ads` or `egyptian_cultural` generation:

```text
EGYPTIAN_LORA_DIR=path/to/egyptian/lora
PRODUCT_LORA_DIR=path/to/product/lora
```

## Run Migrations

From `backend/`:

```bash
alembic upgrade head
```

To generate a new migration after model changes:

```bash
alembic revision --autogenerate -m "initial tables"
alembic upgrade head
```

This project already includes an initial migration for:

- `generations`
- `uploaded_files`
- `chat_messages`

## Run Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend environment example:

```bash
copy .env.example .env
```

Default frontend URL:

```text
http://localhost:5173
```

## AI Backend Zip Usage

The original `visualforge_web_ready_ai_backend.zip` is kept at the project root.

The prepared engine file from the zip is extracted to:

```text
backend/app/ai/visualforge_engine.py
```

The FastAPI app calls the existing engine functions:

- `text_to_image`
- `image_to_image`
- `inpaint`
- `health`

The app only performs inference. Training is not included.

## Logo Usage

- `Logo.png` is the full VisualForge AI logo.
  - Used in the sidebar and full brand placements.
- `Logo2.png` is the icon-only logo.
  - Used for the favicon, chatbot button, collapsed sidebar, and compact brand placements.

Both files are copied into:

```text
frontend/public/
frontend/src/assets/
```

The logo filenames are not changed.

## API Endpoints

Health:

- `GET /health`

Generation:

- `POST /api/text-to-image`
- `POST /api/image-to-image`
- `POST /api/inpaint`

Generation history:

- `GET /api/generations`
- `GET /api/generations/{id}`
- `DELETE /api/generations/{id}`

Uploads:

- `POST /api/uploads`

Analytics:

- `GET /api/analytics/summary`
- `GET /api/analytics/charts`

Chatbot:

- `POST /api/chatbot/message`
- `GET /api/chatbot/history`
- `DELETE /api/chatbot/history`

## Image URL Handling

The AI engine may return local output paths. The backend stores those internal paths as `image_path` and returns browser-safe URLs as `image_url`.

Example response:

```json
{
  "success": true,
  "image_path": "C:/path/to/backend/app/storage/outputs/example.png",
  "image_url": "http://localhost:8000/outputs/example.png",
  "metadata": {
    "mode": "text_to_image",
    "domain": "base",
    "prompt": "studio product render"
  }
}
```

The frontend always displays `image_url`.

## Notes

- Training is not included in the web app.
- The web app only performs inference through the prepared engine.
- The SDXL model is not loaded at FastAPI startup.
- PostgreSQL stores metadata, uploads, generation history, analytics source data, and chatbot messages.
- Images are stored as files and referenced in PostgreSQL.
- The chatbot is rule-based for now. Future LLM/API logic can be added in `backend/app/modules/chatbot/service.py` without changing the frontend structure.
