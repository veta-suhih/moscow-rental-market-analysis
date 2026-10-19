import cianparser

moscow_parser = cianparser.CianParser(location="Москва")
data = moscow_parser.get_flats(
    deal_type="rent_long",
    rooms="all",
    with_saving_csv=False,
    additional_settings={"start_page": 1, "end_page": 1}
)

print(f"✅ Собрано объявлений: {len(data)}")
if data:
    print(data[0])