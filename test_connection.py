import pytest
from playwright.sync_api import Page, expect

@pytest.mark.xfail(reason="Bug connu - voir ticket JIRA : images produits identiques pour problem_user")
def test_images_produits_sont_differentes(page: Page):
    page.goto("https://www.saucedemo.com")
    page.fill("#user-name", "problem_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    images = page.locator(".inventory_item_img img")
    expect(images.first).to_be_visible()  # <- attend que la 1ère image soit bien affichée

    nombre_images = images.count()
    sources = [images.nth(i).get_attribute("src") for i in range(nombre_images)]

    print(f"\nNombre d'images trouvées : {nombre_images}")
    print(f"Sources : {sources}")

    assert len(set(sources)) > 1, f"Toutes les images pointent vers la même source : {sources[0]}"