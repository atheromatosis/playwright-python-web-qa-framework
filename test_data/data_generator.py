from faker import Faker

fake = Faker("en_US")


def generate_valid_contact_payload() -> dict[str, str]:
    """Generate realistic, valid contact form data using Faker."""
    return {
        "full_name": fake.name(),
        "email": fake.safe_email(),
        "phone": fake.numerify("+48 ### ### ###"),
        "message": fake.paragraph(nb_sentences=2),
    }
