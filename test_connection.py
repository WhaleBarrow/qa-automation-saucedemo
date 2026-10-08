import pytest
from playwright.sync_api import Page, expect

URL = "https://www.saucedemo.com"


def se_connecter(page: Page, identifiant: str, mot_de_passe: str):
    page.goto(URL)
    page.fill("#user-name", identifiant)
    page.fill("#password", mot_de_passe)
    page.click("#login-button")


def test_connexion_reussie(page: Page):
    se_connecter(page, "standard_user", "secret_sauce")
    expect(page.locator(".title")).to_have_text("Products")


def test_connexion_mauvais_mot_de_passe(page: Page):
    se_connecter(page, "standard_user", "mauvais_mot_de_passe")
    expect(page.locator("[data-test='error']")).to_be_visible()


@pytest.mark.xfail(reason="Bug connu - voir ticket Jira : images produits identiques pour problem_user")
def test_images_produits_sont_differentes(page: Page):
    se_connecter(page, "problem_user", "secret_sauce")

    images = page.locator(".inventory_item_img img")
    expect(images.first).to_be_visible()  # attend que la page produits soit chargée

    sources = [images.nth(i).get_attribute("src") for i in range(images.count())]

    assert len(set(sources)) > 1, f"Toutes les images pointent vers la même source : {sources[0]}"