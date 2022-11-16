from tkinterGUIS  import connection
from tkinterGUIS  import sessionManager
from tkinterGUIS  import pointDisplay
from classes.mover  import mover


def regPoint():
    if connection.status:
        coord=mover.get_coordinates()
        sessionManager.pointList.append((coord.x,coord.y))
        pointDisplay.displayPoints(sessionManager.pointList)
    pass
def unregPoint():
    sessionManager.pointList.pop()
    pointDisplay.displayPoints(sessionManager.pointList)
    pass