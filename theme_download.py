import requests
import argparse
import json
import pprint

pp = pprint.PrettyPrinter(indent=4)

def shopify_access_header(token):
    return { "X-Shopify-Access-Token": token }

def get_shopify_theme(store, headers):
    url = "https://{0}/admin/themes.json".format(store)

    r = requests.get(url, headers=headers)
    j = r.json()

    themes = j['themes']
    for tt in themes: 
        if tt['role'] == 'main':
            theme_id = tt['id']
            return theme_id

    print("No theme ID found")
    return None

def get_shopify_liquid_assets(store, headers):
    theme_id = get_shopify_theme(store, headers)

    url = "https://{0}/admin/themes/{1}/assets.json".format(store, theme_id)
    r = requests.get(url, headers=headers)
    j = r.json()

    liquid_assets = []
    for aa in j['assets']:
        if aa['content_type'] == 'text/x-liquid':
            liquid_assets.append(aa['key'].encode("utf"))

    pp.pprint(liquid_assets)

def get_shopify_asset(store, headers, asset):
    assert(asset)
    theme_id = get_shopify_theme(store, headers)
    if not theme_id:
        return None

    url = "https://{0}/admin/themes/{1}/assets.json?asset[key]={2}".format(store, theme_id, asset)
    r = requests.get(url, headers=headers)
    j = r.json()

    asset = j['asset']
    liquid = asset['value'].encode("utf")
    print(liquid)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="By default, downloads a list of Liquid file assets in a store's main theme.  If a particular asset is specified, download that file.")
    parser.add_argument("store", help="Store domain e.g. a_shop.myshopify.com")
    parser.add_argument("token", help="Token allowing us access")
    parser.add_argument("--asset", help="Name of theme asset e.g. 'layout/theme.liquid'")

    args = parser.parse_args()

    if not args.token:
        print("You need to supply an access token")
        raise SystemExit

    if not args.store:
        print("You need to supply the store domain")
        raise SystemExit

    headers = shopify_access_header(args.token)
    if args.asset:
        get_shopify_asset(args.store, headers, args.asset)
    else:
        get_shopify_liquid_assets(args.store, headers)





