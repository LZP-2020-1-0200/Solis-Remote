"""Handles traslation between different markers"""

from typing import Any

import numpy as np
from numpy.typing import NDArray

from ..classes.coordinate import Coordinate

def anchor_translate(
        local_anchors:list[Coordinate],
        original_anchors:list[Coordinate],
        original_point:Coordinate
        )->Coordinate:
    """Returns a translated point to local anchors"""
    #generate coords from anchors
    point_a:Coordinate=Coordinate(original_anchors[0].x,original_anchors[0].y)
    point_b:Coordinate=Coordinate(original_anchors[1].x,original_anchors[1].y)
    point_c:Coordinate=Coordinate(original_anchors[2].x,original_anchors[2].y)

    #core vectors
    vector_ab: Coordinate=point_b-point_a
    vector_ac: Coordinate=point_c-point_a

    original_coord:Coordinate=Coordinate(original_point.x,original_point.y)

    # get relative coordinate to A
    relative_og_coord: Coordinate=original_coord-point_a

    aug: NDArray[Any]=np.array([
        [vector_ab.x,vector_ac.x,relative_og_coord.x],
        [vector_ab.y,vector_ac.y,relative_og_coord.y]
    ])
    solved: tuple[float, float]=gaussian_elimination2d(aug)

    #core vectors of this session
    local_ab: Coordinate=local_anchors[1]-local_anchors[0]
    local_ac: Coordinate=local_anchors[2]-local_anchors[0]

    #core vectors multiplied by their scalars create the absolute coordinate
    return local_anchors[0] + (local_ab*solved[0]) + (local_ac*solved[1])

def gaussian_elimination2d(augment_no_type:NDArray[Any])->tuple[float,float]:
    """Performs gaussian elimination on a system of equations
    `augment_no_type` - coeficients of the system
    ```
    arr[0][0]x+arr[0][1]y=arr[0][2]
    arr[1][0]x+arr[1][1]y=arr[1][2]
    ```
    returns `[x,y]`
    """
    augment: NDArray[np.float64]=augment_no_type.astype(np.float64)
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
    assert np.all(np.isclose(gaussian_elimination2d(t),(4.5,2)))#type: ignore

    #[0][0] is 0
    t2:NDArray[Any]=np.array([
        [0,2,8],
        [5,1,9]
    ])
    assert np.all(np.isclose(gaussian_elimination2d(t2),(1,4)))#type: ignore

    #[1][1] is 0
    t3: NDArray[Any]=np.array([
        [4,2,16],
        [2,0,1]
    ])
    assert np.all(np.isclose(gaussian_elimination2d(t3),(0.5,7)))#type: ignore
