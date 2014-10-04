import numpy as np
from np.linalg import norm,inv,lstsq

def hcp(F,Y,h,l1,l2,l3,iters):

    if iters == None:
        iter = 100
    
    l0 = 1
    tol = 10.0**-6

    (n1,k) = F.size
    (n2,g) = Y.size

    Z = np.matrix(n1,h)
    B = np.random.rand(h,g)
    U = np.matrix(k,h)
    obj = np.array(iters)
    
    assert(n1==n2)
    
    if (h<1 or l1<1e-6 or l2<1e-6 or l3<1e-6 ):
        print 'lambda, lambda2, lambda3 must be positive \
                and/or h must be an integer');
    
    delta_epsilon = tol * np.eye(h)
    
    for ii in range(iters):
        obj(ii) = l0*norm(Y-Z*B) + l1* norm(Z-F*U) + l2* norm(B) + l3* norm(U)
        
        Z = (Y*B.transpose() + l1*F*U) * 
            inv(B*B.transpose() + l1*np.eye(h))
        
        B = lstsq((Z.tranpose()*Z + l2*np.eye(h)), Z.tranpose())*Y
        
        U = lstsq(F.transpose()*F*l1 + l3*np.eye(k), l1*F.transpose()*Z)
        
        if ii>0:
            if np.divide(np.fabs(obj(ii)-obj(ii-1)), obj(ii)) < tol:
                 break
    
    e0 = norm(Y-Z*B)/norm(Y) + norm(Z-F*U)/norm(F*U)
    e1 = norm(Y-Z*B)/norm(Y)
    e2 = norm(Z-F*U)/norm(F*U)

    dz = Z*(B*B.transpose() + l1*np.eye(h)) - (Y*B.transpose() + l1*F*U)
    db = (Z.tranpose()*Z + l2*np.eye(h))*B - Z.tranpose()*Y
    du = (F.tranpose()*F*l1 + l3*np.eye(k))*U - l1*F.tranpose()*Z
    
    return (Z,B,U,o)