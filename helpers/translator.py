"""Handles traslation between different markers"""

import numpy as np
from numpy.typing import NDArray
from typing import Any

from classes.coordinate import Coordinate

def anchor_translate(local_anchors:list[Coordinate],original_anchors:list[Coordinate],original_point:Coordinate)->Coordinate:
    """Returns a translated point to local anchors"""
    #generate coords from anchors
    a:Coordinate=Coordinate(original_anchors[0].x,original_anchors[0].y)
    b:Coordinate=Coordinate(original_anchors[1].x,original_anchors[1].y)
    c:Coordinate=Coordinate(original_anchors[2].x,original_anchors[2].y)

    #core vectors
    ab: Coordinate=b-a
    ac: Coordinate=c-a

    ogCoord:Coordinate=Coordinate(original_point.x,original_point.y)

    # get relative coordinate to a
    relOgCoord: Coordinate=ogCoord-a

    aug: NDArray[Any]=np.array([
        [ab.x,ac.x,relOgCoord.x],
        [ab.y,ac.y,relOgCoord.y]
    ])
    solved: tuple[float, float]=gaussianElimination2D(aug)
    

    #core vectors of this session
    abL: Coordinate=local_anchors[1]-local_anchors[0]
    acL: Coordinate=local_anchors[2]-local_anchors[0]

    #core vectors multiplied by their scalars create the absolute coordinate
    return local_anchors[0] + abL*solved[0]+acL*solved[1]

def gaussianElimination2D(augmentNoType:NDArray[Any])->tuple[float,float]:
    augment: NDArray[np.float64]=augmentNoType.astype(np.float64)
    #swap 
    if abs(augment[0][0])<abs(augment[1][0]) or augment[1][1]==0:
        augment[[0,1]]=augment[[1,0]]
    #normalize first pivot    
    augment[0]=augment[0]/augment[0][0]
    #zero out 1st element of 2nd row
    augment[1]=augment[1]-(augment[0]*augment[1][0])
    #normalize 2nd pivot 
    augment[1]=augment[1]/augment[1][1]
    #zero out 2nd element of 1st row
    augment[0]=augment[0]-(augment[1]*augment[0][1])
    return (augment[0][2],augment[1][2])


if __name__=="__main__":
    #-------test cases-------

    #normal case
    t: NDArray[Any]=np.array([
        [2,3,15],
        [3,0.5,14.5]
    ])
    assert np.all(np.isclose(gaussianElimination2D(t),(4.5,2)))#type: ignore

    #[0][0] is 0
    t2:NDArray[Any]=np.array([
        [0,2,8],
        [5,1,9]
    ])
    assert np.all(np.isclose(gaussianElimination2D(t2),(1,4)))#type: ignore

    #[1][1] is 0
    t3: NDArray[Any]=np.array([
        [4,2,16],
        [2,0,1]
    ])
    assert np.all(np.isclose(gaussianElimination2D(t3),(0.5,7)))#type: ignore
    
    
