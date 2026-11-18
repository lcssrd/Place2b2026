import json, urllib.request, urllib.parse, ssl, sys
ctx = ssl.create_default_context(cafile='/root/.ccr/ca-bundle.crt')
towns = [('76290','Montivilliers'),('76700','Harfleur'),('76430','Saint-Romain-de-Colbosc'),('76110','Goderville'),('76790','Étretat'),
 ('76450','Cany-Barville'),('76460','Saint-Valery-en-Caux'),('76560','Doudeville'),('76890','Tôtes'),('76570','Pavilly'),('76480','Duclair'),
 ('76690','Clères'),('76750','Buchy'),('76680','Saint-Saëns'),('76440','Forges-les-Eaux'),('76160','Darnétal'),('76230','Bois-Guillaume'),
 ('76130','Mont-Saint-Aignan'),('76150','Maromme'),('76530','Grand-Couronne'),('27310','Bourg-Achard'),('27500','Pont-Audemer'),('27400','Louviers'),
 ('76550','Offranville'),('76630','Envermeu'),('76000','Rouen'),('76600','Le Havre')]
streets = ['rue de la République','rue du Général de Gaulle','rue Jean Jaurès','Grande Rue','rue Victor Hugo','rue Gambetta','rue Pasteur','rue Carnot']
out = {}
for cp, town in towns:
    for i, s in enumerate(streets):
        q = f'{4+2*i} {s}, {cp} {town}'
        u = 'https://data.geopf.fr/geocodage/search?' + urllib.parse.urlencode({'q': q, 'limit': 1})
        import time; time.sleep(0.25)
        try: f = json.load(urllib.request.urlopen(u, context=ctx, timeout=15))['features']
        except Exception as e: print('err', q, e); continue
        if f and f[0]['properties']['score'] > 0.6 and f[0]['properties']['type'] in ('housenumber', 'street') and f[0]['properties']['postcode'] == cp:
            out[town] = q; print('OK ', q, round(f[0]['properties']['score'], 2)); break
    else: print('-- ', town)
json.dump(out, open('data/addr-ok.json', 'w'), ensure_ascii=False, indent=1)
