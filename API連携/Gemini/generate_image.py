from google import genai
from google.genai import types
import os
import sys
from datetime import datetime

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", "AIzaSyDk3qZznYlKsX6lmMUMjGrNcsqf9lrTOsI"))

def generate_image(prompt, output_folder, filename):
    response = client.models.generate_images(
        model='imagen-3.0-generate-002',
        prompt=prompt,
        config=types.GenerateImagesConfig(number_of_images=1)
    )
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"{output_folder}/{timestamp}_{filename}.png"

    image = response.generated_images[0]
    with open(output_path, "wb") as f:
        f.write(image.image.image_bytes)

    print(f"画像生成完了：{output_path}")
    return output_path

def generate_text(prompt):
    """テキスト生成（画像プロンプト作成などに使用）"""
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    return response.text

if __name__ == "__main__":
    prompt = sys.argv[1] if len(sys.argv) > 1 else "テスト画像"
    folder = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser("~/Desktop/AI経営本部/集客販売/Instagram動画原稿")
    os.makedirs(folder, exist_ok=True)
    generate_image(prompt, folder, "generated")
