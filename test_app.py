from app import app

def test_header_present(dash_duo):
    dash_duo.start_server(app)
    dash_duo.wait_for_element("h1.title", timeout=10)
    assert dash_duo.find_element("h1.title").text == "Soul Foods Analytics"

def test_visualization_present(dash_duo):
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#sales-chart", timeout=10)

def test_region_picker_present(dash_duo):
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#region-filter", timeout=10)
