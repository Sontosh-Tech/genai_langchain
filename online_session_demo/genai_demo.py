
# Generative AI - Text and Image Generation
from transformers import pipeline
import torch

# Text Generation (GPT-2)
text_gen = pipeline("text-generation", model="gpt2")
print(text_gen("Once upon a time", max_length=50)[0]['generated_text'])

# Image Generation - using diffusers
from diffusers import StableDiffusionPipeline
pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", torch_dtype=torch.float16)
#pipe.to("cuda")
pipe.to("cpu")

prompt = "a futuristic city at sunset"
image = pipe(prompt).images[0]
image.save("generated_image.png")