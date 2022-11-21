from tkinterGUIS  import connection
from tkinterGUIS  import sessionManager
from tkinterGUIS  import pointDisplay
from classes.mover  import mover


def regPoint():
    """Adds a point and displays it"""
    if connection.getStatus():
        coord=mover.get_coordinates()
        sessionManager.pointList.append((coord.x,coord.y))
        pointDisplay.displayPoints()
    pass
def unregPoint():
    """Removes the point from memory and screen"""
    sessionManager.pointList.pop()
    pointDisplay.displayPoints()
    pass