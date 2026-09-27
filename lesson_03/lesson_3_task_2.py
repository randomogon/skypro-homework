from smartphone import Smartphone


catalog = [
    Smartphone("Apple", "iPhone 16", "+79111111111"),
    Smartphone("Samsung", "Galaxy S25", "+79222222222"),
    Smartphone("Xiaomi", "14", "+79333333333"),
    Smartphone("Google", "Pixel 9", "+79444444444"),
    Smartphone("OnePlus", "13", "+79555555555"),
]

for phone in catalog:
    print(f"{phone.brand} - {phone.model}. {phone.phone_number}")
