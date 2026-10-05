import io
import qrcode
import cloudinary.uploader
import cloudinary.utils


def create_transformed_picture_url(public_id: str, width: int = 500, height: int = 500, crop: str = "fill") -> str:
    """Генерує URL трансформованого зображення через Cloudinary."""
    url, _ = cloudinary.utils.cloudinary_url(
        public_id,
        width=width,
        height=height,
        crop=crop,
        secure=True
    )
    return url


def generate_qr_code_url(target_url: str) -> str:
    """Генерує QR-код для заданого URL і завантажує його в Cloudinary."""
    # Створення QR-коду в пам'яті
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(target_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    # Збереження зображення в байтовий потік
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Завантаження QR-коду в Cloudinary
    result = cloudinary.uploader.upload(
        buffer,
        folder="photoshare_qrcodes",
        resource_type="image"
    )
    return result.get("secure_url")