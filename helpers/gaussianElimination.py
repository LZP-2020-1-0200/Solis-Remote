import numpy as np
def gaussianElimination2D(aug):
    aug=aug.astype(np.float64)
    #swap 
    if abs(aug[0][0])<abs(aug[1][0]) or aug[1][1]==0:
        aug[[0,1]]=aug[[1,0]]
    #normalize first pivot    
    aug[0]=aug[0]/aug[0][0]
    #zero out 1st element of 2nd row
    aug[1]=aug[1]-(aug[0]*aug[1][0])
    #normalize 2nd pivot 
    aug[1]=aug[1]/aug[1][1]
    #zero out 2nd element of 1st row
    aug[0]=aug[0]-(aug[1]*aug[0][1])
    return (aug[0][2],aug[1][2])


if __name__=="__main__":
    #-------test cases-------

    #normal case
    t=np.array([
        [2,3,15],
        [3,0.5,14.5]
    ])
    assert np.all(np.isclose(gaussianElimination2D(t),(4.5,2)))

    #[0][0] is 0
    t2=np.array([
        [0,2,8],
        [5,1,9]
    ])
    assert np.all(np.isclose(gaussianElimination2D(t2),(1,4)))

    #[1][1] is 0
    t3=np.array([
        [4,2,16],
        [2,0,1]
    ])
    assert np.all(np.isclose(gaussianElimination2D(t3),(0.5,7)))
    
    
