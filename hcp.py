import numpy as np
from numpy.linalg import norm,inv,lstsq
from numpy import matlib

def hcp(F,Y,h,l1,l2,l3,iters):

    if iters == None:
        iter = 100
    
    l0 = 1
    tol = 10.0**-6
    
    # Number of rows and columns in F
    fRows = F.shape[0]
    fCols = F.shape[1]

    # Matrix U is dimension fCols by h and is populated with 0's
    U = np.zeros((fCols,h))
    # Matrix Z is dimension fRows by h and is populated with 0's.
    Z = np.zeros((fRows,h))
    
    # Number of columns of Z and Y
    zCols = Z.shape[1]
    yCols = Y.shape[1]
    
    # Create a zCols by yCols matrix with random values from 0-1
    B = np.random.rand(zCols, yCols)

    # Creates a 1-Dimensonal array with "iters" number of indices
    obj = np.zeros( (iters, 1) )

    yRows = Y.shape[0]   # Number of rows in Y 
    
    assert(fRows == yRows), "Number of rows in F and Y must agree."
    
    if (h<1 or l1<1e-6 or l2<1e-6 or l3<1e-6 ):
        print 'l1, l2, l3 must be positive and/or h must be an integer.';
    
    for ii in range(iters):
        
        obj[ii] = np.sum(np.sum((Y - np.dot(Z,B))**2))     \
                + np.sum(np.sum((Z - np.dot(F,U))**2))* l1 \
                + np.sum(np.sum(B**2)) * l2                \
                + np.sum(np.sum(U**2) * l3);
        
        Z = np.dot( np.dot(Y, B.transpose()) + l1 * np.dot(F,U) , \
                   inv( np.dot(B, B.transpose()) + l1 * np.eye(h)) )

        least_squares_solution = lstsq( np.dot(Z.transpose() , Z) \
                                       + l2 * np.eye(zCols), Z.transpose() )
        B =  np.dot(least_squares_solution[0], Y)
        
        # Number of rows in U
        uRows = U.shape[0]   
        U = lstsq( np.dot(F.transpose(),F ) * l1 + l3 * np.eye(uRows), \
                  l1 * np.dot(F.transpose(),Z) )
        # Extract desired matrix out of tuple
        U = U[0]   
        
        if ii > 0:
            if np.divide(np.fabs(obj[ii] - obj[ii-1]), obj[ii]) < tol:
                 break
        
    # Unused (e0, e1, e2), but included in case useful in future. If it does not produce the intended
    # results, view original hcp.m code. They use a series of sums instead of norms.
    # e0 = norm(Y - np.dot(Z,B) ) / norm(Y) + norm(Z - np.dot(F,U)) / norm( np.dot(F,U) )
    # e1 = norm(Y - np.dot(Z,B) ) / norm(Y)
    # e2 = norm(Z - np.dot(F,U) ) / norm( np.dot(F,U) )

    # Unused (dz, db, du), but included in case useful in the future.
    # bRows = B.shape[0]   # Number of rows in B
    # zCols = Z.shape[1]   # Number of columns in Z
    # uRows = U.shape[0]   # Number of rows in U
    # dz = np.dot(Z, ( np.dot(B,B.transpose()) + l1*np.eye(bRows) ) ) - ( np.dot(Y,B.transpose() ) + l1* np.dot(F,U) )
    # db = np.dot( np.dot(Z.transpose(),Z) + l2* np.eye(zCols),B) - np.dot(Z.transpose(),Y)
    # du = np.dot( np.dot(F.transpose(),F)*l1 + l3* np.eye(uRows),U) - l1* np.dot(F.transpose(),Z)
    
    return (Z,B,U,obj)
