"""Many of the tests were derived from here:

http://www.maptiler.org/google-maps-coordinates-tile-bounds-projection/
"""
import pytest

from tiletanic.tileschemes import WebMercatorBL

@pytest.fixture
def tiler():
    return WebMercatorBL()


def test_bounds(tiler):
    """Web Mercator bounds."""
    assert tiler.bounds.xmin == -20037508.342789244
    assert tiler.bounds.xmax == 20037508.342789244
    assert tiler.bounds.ymin == -20037508.342789244
    assert tiler.bounds.ymax == 20037508.342789244

    
def test_tile(tiler):
    """Tile generation from gespatial coordinates and zoom."""
    assert tiler.tile(0., 0., 0) == (0, 0, 0)

    assert tiler.tile((-20037508.342789244 + -10018754.171394622)/2.,
                      (-20037508.342789244 + -10018754.171394622)/2.,
                      2) == (0, 0, 2)

    assert tiler.tile((-12523442.714243278 + -10018754.171394622)/2.,
                      (5009377.085697312 + 7514065.628545966)/2.,
                      4) == (3, 10, 4)
    
    assert tiler.tile((13492052.736673031 + 13494498.721578155)/2.,
                      (1849164.5882749856 + 1851610.5731801093)/2.,
                      14) == (13708, 8948, 14)


def test_parent(tiler):
    """Parent of a tile."""
    assert tiler.parent(0, 0, 1) == (0, 0, 0)
    assert tiler.parent(1, 0, 1) == (0, 0, 0)

    assert tiler.parent(2, 3, 2) == (1, 1, 1)
    assert tiler.parent(3, 0, 2) == (1, 0, 1)


def test_children1(tiler):
    """Children of a level 0 tile."""
    assert set(tiler.children(0, 0, 0)) == {(0, 0, 1),
                                            (1, 0, 1),
                                            (0, 1, 1),
                                            (1, 1, 1)}

    
def test_children2(tiler):
    """Children of a level > 0 tile."""
    assert set(tiler.children(1, 1, 1)) == {(2, 2, 2),
                                            (2, 3, 2),
                                            (3, 2, 2),
                                            (3, 3, 2)}
    

def test_quadkey(tiler):
    "Quadkey generation from tile coordinates."""
    assert tiler.quadkey(0, 0, 1) == '0'
    assert tiler.quadkey(1, 0, 1) == '1'

    assert tiler.quadkey(0, 0, 2) == '00'
    assert tiler.quadkey(1, 0, 2) == '01'
    assert tiler.quadkey(0, 1, 2) == '02'
    assert tiler.quadkey(1, 1, 2) == '03'
    assert tiler.quadkey(2, 0, 2) == '10'
    assert tiler.quadkey(3, 0, 2) == '11'
    assert tiler.quadkey(2, 1, 2) == '12'
    assert tiler.quadkey(3, 1, 2) == '13'

    assert tiler.quadkey(20, 35, 9) == '000210122'

        
def test_ul(tiler):
    """Upper left coordinates of input tile."""
    assert tiler.ul(0, 0, 1) == (-20037508.342789244, 0.0)
    assert tiler.ul(1, 0, 1) == (0.0, 0.0)
    
    assert tiler.ul(3, 1, 3) == (-5009377.085697312, -10018754.171394622)
    assert tiler.ul(4, 1, 3) == (0.0, -10018754.171394622)
    assert tiler.ul(3, 2, 3) == (-5009377.085697312, -5009377.085697312)
    assert tiler.ul(4, 2, 3) == (0.0, -5009377.085697312)
    
    
def test_br(tiler):
    """Bottom right coordinates of input tile."""
    assert tiler.br(0, 1, 1) == (0.0, 0.0)
    assert tiler.br(1, 1, 1) == (20037508.342789244, 0.0)
    
    assert tiler.br(3, 1, 3) == (0.0, -15028131.257091932)
    assert tiler.br(4, 1, 3) == (5009377.085697312, -15028131.257091932)
    assert tiler.br(3, 2, 3) == (0.0, -10018754.171394622)
    assert tiler.br(4, 2, 3) == (5009377.085697312, -10018754.171394622)


def test_bbox(tiler):   
    """Bounding boxes of tiles."""
    assert tiler.bbox(0, 0, 1) == (-20037508.342789244, -20037508.342789244, 0.0, 0.0)
    assert tiler.bbox(1, 0, 1) == (0.0, -20037508.342789244, 20037508.342789244, 0.0)
                                   
    assert tiler.bbox(3, 1, 3) == (-5009377.085697312, -15028131.257091932, 0.0, -10018754.171394622)
    assert tiler.bbox(4, 1, 3) == (0, -15028131.257091932, 5009377.085697312, -10018754.171394622)
    assert tiler.bbox(3, 2, 3) == (-5009377.085697312, -10018754.171394622, 0.0, -5009377.085697312)
    assert tiler.bbox(4, 2, 3) == (0.0, -10018754.171394622, 5009377.085697312, -5009377.085697312)
                                   

    
def test_quadkey(tiler):
    """Tile to quadkey."""
    assert not tiler.quadkey(0, 0, 0)

    assert tiler.quadkey(3, 1, 3) == '231'
    assert tiler.quadkey(4, 1, 3) == '320'
    assert tiler.quadkey(3, 2, 3) == '213'
    assert tiler.quadkey(4, 2, 3) == '302'

    assert tiler.quadkey(199744, 179200, 18) == '130200112223222222'
    assert tiler.quadkey(84201, 103979, 18) == '210320300233121201' 

def test_quadkey_to_tile1(tiler):
    """Quadkey to tile exceptions."""
    with pytest.raises(ValueError):
        tiler.quadkey_to_tile('4')

    
def test_quadkey_to_tile2(tiler):
    """Quadkey to tile."""
    assert tiler.quadkey_to_tile('0') == (0, 1, 1)
    assert tiler.quadkey_to_tile('130232101') == (405, 327, 9)
    assert tiler.quadkey_to_tile('130200112223222222') == (199744, 179200, 18)
    assert tiler.quadkey_to_tile('210320300233121201') == (84201, 103979, 18)
