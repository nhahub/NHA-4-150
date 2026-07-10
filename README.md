\# VisualForge AI  

\## An End-to-End AI Visual Content Generation Studio



VisualForge AI is an academic AI project that builds a complete visual content generation studio using Stable Diffusion XL, LoRA fine-tuning, and an interactive demo interface.



The system supports Text-to-Image generation, Image-to-Image transformation, and Inpainting, with domain-based generation for product advertising and Egyptian cultural visual styles.



\---



\## Team Members



\- Basel Abdel Maqsoud Abdel Maqsoud Ziada  

\- Sherif Mohamed Hassan Mohamed  

\- Ahmed Gaber Ahmed Elsadek  

\- Youssef Ahmed Mohammed Saed  



\---



\## Project Overview



AI image generation tools are powerful, but many of them are either too general, difficult to control, or not specialized for specific creative domains.



VisualForge AI solves this problem by providing a complete workflow that allows users to generate, edit, and refine images using:



\- Text prompts

\- Uploaded source images

\- Mask images

\- Creative domain selection

\- Stable Diffusion XL

\- Fine-tuned LoRA adapters

\- A simple Gradio demo interface

\- A full web application prototype



The project was developed as an end-to-end AI visual generation system, starting from problem definition, model selection, dataset preparation, LoRA fine-tuning, interface development, testing, and final presentation.



\---



\## Problem Statement



Most AI image generation platforms provide general image generation, but they often lack specialization for specific creative use cases.



The main problems addressed by this project are:



\- Difficulty generating domain-specific visual content

\- Need for a simple interface instead of code-based notebooks

\- Need for multiple generation modes in one system

\- Need for image editing and refinement

\- Need for specialized visual styles such as product advertising and Egyptian cultural design

\- Difficulty connecting fine-tuned AI models to a usable demo interface



\---



\## Project Objective



The objective of VisualForge AI is to build a practical AI-powered visual generation studio that can:



\- Generate images from text prompts

\- Transform existing images using prompts

\- Edit selected image regions using inpainting

\- Support domain-based generation

\- Use fine-tuned LoRA adapters for specialized domains

\- Provide a user-friendly demo interface

\- Prepare a web-based prototype for future deployment



\---



\## Core Features



\- Text-to-Image generation

\- Image-to-Image transformation

\- Inpainting / image editing

\- Domain-based generation

\- Product Ads LoRA

\- Egyptian Cultural LoRA

\- Gradio demo interface

\- Gallery for generated outputs

\- Downloadable generated images

\- Web application prototype using React, FastAPI, and PostgreSQL



\---



\## Generation Modes



\### 1. Text-to-Image



Generates a new image from a text prompt.



Example:



```text

A modern perfume bottle on a dark futuristic background, cinematic lighting, high quality

```



\### 2. Image-to-Image



Transforms an uploaded image according to a prompt and selected creative domain.



Example:



```text

Transform this image into a professional luxury product advertisement with studio lighting and a premium commercial look

```



\### 3. Inpainting



Edits a selected or masked area in an uploaded image using a prompt.



Example:



```text

Replace the masked area with ancient Egyptian golden patterns and cinematic cultural details

```



\---



\## Models and Pipelines Used



\### Base Model



Stable Diffusion XL Base 1.0 was used as the main generative model.



Model link:



https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0



\### Diffusers Pipelines



Stable Diffusion XL pipelines were used through Hugging Face Diffusers.



Documentation link:



https://huggingface.co/docs/diffusers/en/api/pipelines/stable\_diffusion/stable\_diffusion\_xl



Used pipelines:



\- `StableDiffusionXLPipeline` for Text-to-Image

\- `StableDiffusionXLImg2ImgPipeline` for Image-to-Image

\- `StableDiffusionXLInpaintPipeline` for Inpainting



\---



\## Fine-Tuning Method



The project uses LoRA fine-tuning to adapt Stable Diffusion XL to specific creative domains without retraining the full model.



LoRA was selected because it is more efficient than full fine-tuning and is suitable for limited GPU environments such as Kaggle.



Instead of training the entire SDXL model again, LoRA trains lightweight adapter weights that can be loaded on top of the base model.



\---



\## Fine-Tuned Domains



Two main domains were selected for fine-tuning:



1\. Product Ads

2\. Egyptian Cultural



These domains were selected because they have clear visual styles and practical use cases.



\---



\## Product Ads LoRA



\### Purpose



The Product Ads domain focuses on generating professional product advertisement visuals.



It is designed to improve:



\- Commercial product composition

\- Studio lighting

\- Premium branding style

\- Clean backgrounds

\- Product photography quality

\- Advertising-style visual outputs



\### Trigger Word



```text

vforge\_product\_ad\_style

```



\### LoRA Output File



```text

product\_ads\_lora\_300.safetensors

```



\### Dataset Used



Dataset name:



```text

ashraq/fashion-product-images-small

```



Dataset link:



https://huggingface.co/datasets/ashraq/fashion-product-images-small



\### Used For



\- Product Ads LoRA fine-tuning

\- Commercial-style image generation

\- Product-focused visual content



\---



\## Egyptian Cultural LoRA



\### Purpose



The Egyptian Cultural domain focuses on generating Egyptian cultural and heritage-inspired visuals.



It is designed to add:



\- Ancient Egyptian motifs

\- Heritage-inspired visual details

\- Cultural atmosphere

\- Warm cinematic lighting

\- Egyptian design elements

\- Cultural identity in generated images



\### Trigger Word



```text

vforge\_egyptian\_cultural\_style

```



\### LoRA Output File



```text

pytorch\_lora\_weights\_500.safetensors

```



\### Dataset Used



Dataset name:



```text

IMATOR/Ancient\_Egyptians\_model

```



Dataset link:



https://huggingface.co/datasets/IMATOR/Ancient\_Egyptians\_model



\### Used For



\- Egyptian Cultural LoRA fine-tuning

\- Cultural image generation

\- Heritage-inspired visual content



\---



\## Proposed Domains



During the planning phase, several creative domains were proposed:



\- General / Base

\- Product Ads

\- Egyptian Cultural

\- Architecture / Interior Design

\- Fashion Visuals

\- Social Media Content



The domains selected for fine-tuning were:



\- Product Ads

\- Egyptian Cultural



The other domains are considered future extensions.



\---



\## System Workflow



The system follows this workflow:



```text

User Input

↓

Generation Mode Selection

↓

Creative Domain Selection

↓

Stable Diffusion XL Base Model

↓

Optional LoRA Adapter

↓

Generated Output

↓

Gallery / Download

```



\---



\## Repository Structure



```text

NHA-4-150/

│

├── notebooks/

│   └── An\_End\_to\_End\_AI\_Visual\_Content\_Generation\_Studio.ipynb

│

├── gradio\_demo/

│   └── gradio\_app.py

│

├── presentation/

│   └── VisualForge\_AI\_Presentation.pptx

│

├── web/

│   └── visualforge-ai/

│       ├── frontend/

│       ├── backend/

│       └── docker-compose.yml

│

├── docs/

├── .gitignore

└── README.md

```



\---



\## Gradio Demo



The Gradio demo runs the real SDXL model on Kaggle GPU and supports:



\- General / Base generation

\- Product Ads LoRA

\- Egyptian Cultural LoRA

\- Text-to-Image

\- Image-to-Image

\- Inpainting

\- Gallery of generated outputs



Run the demo from Kaggle or a GPU environment:



```bash

python gradio\_demo/gradio\_app.py

```



The demo uses `share=True` to generate a public Gradio link for testing.



\---



\## Web Prototype



The project also includes a full web application prototype.



The web prototype was built using:



\- React

\- Vite

\- Tailwind CSS

\- FastAPI

\- PostgreSQL

\- SQLAlchemy

\- Docker Compose



The web version includes:



\- Dashboard

\- Studio page

\- Gallery

\- Settings

\- Backend API

\- Database integration

\- Mock AI testing

\- Real AI integration experiments



\---



\## Local Web Project Notes



The web prototype was used to test the full application flow:



```text

Frontend

↓

FastAPI Backend

↓

PostgreSQL Database

↓

AI Service Layer

↓

Gallery and Analytics

```



The local system was tested using mock AI mode first to validate:



\- Frontend forms

\- Backend endpoints

\- File uploads

\- Database storage

\- Gallery updates

\- Analytics updates



Then real AI experiments were attempted using local GPU and Kaggle GPU.



\---



\## Testing



The system was tested using the following scenarios:



\### Test 1: Text-to-Image / General Base



Prompt:



```text

A futuristic AI workstation in a dark room, glowing blue screens, cinematic lighting, ultra detailed, high quality

```



Expected result:



\- SDXL generates a real image

\- No LoRA is applied

\- Output is saved to the gallery



\---



\### Test 2: Text-to-Image / Product Ads LoRA



Prompt:



```text

A luxury perfume bottle on a glossy black surface, elegant product photography, premium advertising campaign, soft reflections, cinematic lighting

```



Expected result:



\- Product Ads LoRA is activated

\- Output follows commercial product advertisement style

\- Image is saved to the gallery



\---



\### Test 3: Text-to-Image / Egyptian Cultural LoRA



Prompt:



```text

A majestic ancient Egyptian temple entrance at sunset, golden light, cultural heritage design, cinematic atmosphere, highly detailed

```



Expected result:



\- Egyptian Cultural LoRA is activated

\- Output includes Egyptian cultural visual elements

\- Image is saved to the gallery



\---



\### Test 4: Image-to-Image / Product Ads



Prompt:



```text

Transform this image into a professional luxury product advertisement with studio lighting, clean background, premium commercial look

```



Expected result:



\- Uploaded image is transformed

\- Product Ads domain style is applied

\- Output is saved to the gallery



\---



\### Test 5: Inpainting / Egyptian Cultural



Prompt:



```text

Replace the masked area with ancient Egyptian golden patterns and cinematic cultural details

```



Expected result:



\- The masked area is edited

\- Egyptian cultural visual style is applied

\- Output is saved to the gallery



\---



\## Important Notes



Large AI model weights and generated outputs are not pushed to GitHub.



The following files are excluded from the repository:



\- `.env`

\- `node\_modules`

\- `venv`

\- generated outputs

\- uploaded files

\- `.safetensors` model weights

\- model checkpoints

\- temporary Kaggle outputs



This keeps the repository clean, lightweight, and safe.



\---



\## Why Model Weights Are Not Included



The LoRA and model files are large and should not be pushed directly to GitHub.



Instead, the repository provides:



\- Source code

\- Notebook

\- Demo interface

\- Presentation

\- Dataset links

\- Model links

\- Fine-tuning details



The LoRA weights can be stored externally or uploaded using platforms such as Kaggle, Hugging Face, or Google Drive if needed.



\---



\## Technologies Used



\- Python

\- PyTorch

\- Hugging Face Diffusers

\- Stable Diffusion XL

\- LoRA fine-tuning

\- Gradio

\- Kaggle GPU

\- React

\- Vite

\- Tailwind CSS

\- FastAPI

\- PostgreSQL

\- SQLAlchemy

\- Docker Compose



\---



\## Project Results



The project successfully produced:



\- A complete AI image generation workflow

\- A working Gradio demo

\- SDXL-based Text-to-Image generation

\- Image-to-Image transformation

\- Inpainting

\- Product Ads LoRA

\- Egyptian Cultural LoRA

\- Output gallery

\- Web application prototype

\- Final academic presentation



\---



\## Future Work



Future improvements include:



\- Deploying the Gradio demo permanently

\- Reconnecting the full React + FastAPI web application to a GPU backend

\- Adding more fine-tuned creative domains

\- Adding authentication and user history

\- Adding chatbot assistant for prompt improvement

\- Improving gallery and project management features

\- Hosting LoRA adapters on Hugging Face or another model hub

\- Adding cloud GPU deployment support



\---



\## Conclusion



VisualForge AI demonstrates a complete end-to-end AI visual content generation workflow.



The project combines Stable Diffusion XL, LoRA fine-tuning, multiple image generation modes, domain-based generation, and interactive demo interfaces to create a practical AI-powered visual generation studio.



It started from problem definition and progressed through solution design, dataset selection, fine-tuning, web prototyping, Gradio deployment, testing, and final presentation.

