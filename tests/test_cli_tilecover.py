from click.testing import CliRunner

from tiletanic import cli

def test_cover_geometry_dgtiling_level_9_feature_collection():
    # Wall South Dakota AOI from geojson.io:
    #http://bl.ocks.org/d/fbc0b6427b48274c1782
    #http://bl.ocks.org/anonymous/raw/fbc0b6427b48274c1782/map.geojson
    wall_south_dakota_aoi = '{"type":"FeatureCollection","features":[{"geometry":{"type":"Polygon","coordinates":[[[-101.953125,43.59375],[-101.953125,44.296875],[-102.65625,44.296875],[-102.65625,43.59375],[-101.953125,43.59375]]]},"type":"Feature","properties":{}}]}'

    runner = CliRunner()
    result = runner.invoke(cli.cover_geometry, ['-'], input=wall_south_dakota_aoi)

    assert result.exit_code == 0
    assert result.output == "021323330\n"

def test_cover_geometry_dgtiling_level_9_feature():
    # Wall South Dakota AOI from geojson.io:
    #http://bl.ocks.org/d/fbc0b6427b48274c1782
    #http://bl.ocks.org/anonymous/raw/fbc0b6427b48274c1782/map.geojson
    wall_south_dakota_aoi = '{"geometry":{"coordinates":[[[ -101.953125,43.59375],[-101.953125,44.296875],[-102.65625,44.296875],[-102.65625,43.59375],[-101.953125,43.59375]]],"type":"Polygon"},"type":"Feature"}'

    runner = CliRunner()
    result = runner.invoke(cli.cover_geometry, ['-'], input=wall_south_dakota_aoi)

    assert result.exit_code == 0
    assert result.output == "021323330\n"


def test_cover_geometry_dgtiling_level_9_adajcent_tiles():
    # Wall South Dakota AOI from geojson.io:
    #http://bl.ocks.org/d/fbc0b6427b48274c1782
    #http://bl.ocks.org/anonymous/raw/fbc0b6427b48274c1782/map.geojson
    wall_south_dakota_aoi = '{"geometry":{"coordinates":[[[ -101.953125,43.59375],[-101.953125,44.296875],[-102.65625,44.296875],[-102.65625,43.59375],[-101.953125,43.59375]]],"type":"Polygon"},"type":"Feature"}'

    runner = CliRunner()
    result = runner.invoke(cli.cover_geometry, ['--adjacent', '-'], input=wall_south_dakota_aoi)

    assert result.exit_code == 0
    assert result.output == "021323303\n021323312\n021323313\n021323321\n021323323\n021323330\n021323331\n021323332\n021323333\n"

def test_cover_geometry_dgtiling_6_level_9_partitions():
    # 6-partition Denver metro area AOI
    #http://bl.ocks.org/d/32778deffa5e2043376b
    #http://bl.ocks.org/anonymous/raw/32778deffa5e2043376b/map.geojson
    denver_aoi = '{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[-105.47973632812499,39.59510684995191],[-105.47973632812499,40.25856876391262],[-104.60357666015625,40.25856876391262],[-104.60357666015625,39.59510684995191],[-105.47973632812499,39.59510684995191]]]}}]}'

    runner = CliRunner()
    result = runner.invoke(cli.cover_geometry, ['-'], input=denver_aoi)

    assert result.exit_code == 0
    assert result.output == "021323001\n021323003\n021323010\n021323011\n021323012\n021323013\n"
