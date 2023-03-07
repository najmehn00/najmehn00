import random
import numpy
import math
import time

                
def move(PopSize,dim,pos,vel,acc):
    for i in range(0,PopSize):
        for j in range (0,dim):
            r1=random.random()
            vel[i,j]=r1*vel[i,j]+acc[i,j]
            pos[i,j]=pos[i,j]+vel[i,j]
    
    return pos, vel
def massCalculation(fit,PopSize,M):
    Fmax = max(fit)
    Fmin = min(fit)
    Fsum = sum(fit)        
    Fmean = Fsum/len(fit)
        
    if Fmax == Fmin:
        M = numpy.ones(PopSize)
    else:
        best = Fmin
        worst = Fmax
        
        for p in range(0,PopSize):
           M[p] = (fit[p]-worst)/(best-worst)
            
    Msum=sum(M)
    for q in range(0,PopSize):
        M[q] = M[q]/Msum
            
    return M

def gField(PopSize,dim,pos,M,l,iters,G,ElitistCheck,Rpower):
    final_per = 2
    if ElitistCheck == 1:
        kbest = final_per + (1-l/iters)*(100-final_per)
        kbest = round(PopSize*kbest/100)
    else:
        kbest = PopSize
            
    kbest = int(kbest)
    ds = sorted(range(len(M)), key=lambda k: M[k],reverse=True)
        
    Force = numpy.zeros((PopSize,dim))
   
    
    for r in range(0,PopSize):
        for ii in range(0,kbest):
            z = ds[ii]
            R = 0
            if z != r:                    
                x=pos[r,:]
                y=pos[z,:]
                esum=0
                imval = 0
                for t in range(0,dim):
                    imval = ((x[t] - y[t])** 2)
                    esum = esum + imval
                    
                R = math.sqrt(esum)
                
                for k in range(0,dim):
                    randnum=random.random()
                    Force[r,k] = Force[r,k]+randnum*(M[z])*((pos[z,k]-pos[r,k])/(R**Rpower+numpy.finfo(float).eps))
                    
    acc = numpy.zeros((PopSize,dim))
    for x in range(0,PopSize):
        for y in range (0,dim):
            acc[x,y]=Force[x,y]*G
    return acc
def gConstant(l,iters):
    alfa = 20
    G0 = 100
    Gimd = numpy.exp(-alfa*float(l)/iters)
    G = G0*Gimd
    return G
        
def GSA(objf,lb,ub,dim,PopSize,iters):
    # GSA parameters
    ElitistCheck =1
    Rpower = 1 
     
        
    """ Initializations """
    
    vel=numpy.zeros((PopSize,dim))
    fit = numpy.zeros(PopSize)
    M = numpy.zeros(PopSize)
    gBest=numpy.zeros(dim)
    gBestScore=float("inf")
    
    pos=numpy.random.uniform(0,1,(PopSize,dim)) *(ub-lb)+lb
    
    convergence_curve=numpy.zeros(iters)
    
    print("Start GSA  optimizing on sphere  ")    
    
    for l in range(0,iters):
        for i in range(0,PopSize):
            l1 = [None] * dim
            l1=numpy.clip(pos[i,:], lb, ub)
            pos[i,:]=l1

            #Calculate objective function for each mass
            fitness=[]
            fitness=objf(l1)
            fit[i]=fitness
    
                
            if(gBestScore>fitness):
                gBestScore=fitness
                gBest=l1           
        
        """ Calculating Mass """
        M = massCalculation(fit,PopSize,M)

        """ Calculating Gravitational Constant """        
        G = gConstant(l,iters)        
        
        """ Calculating Gfield """        
        acc = gField(PopSize,dim,pos,M,l,iters,G,ElitistCheck,Rpower)
        
        """ Calculating Position """        
        pos, vel = move(PopSize,dim,pos,vel,acc)
        
        convergence_curve[l]=gBestScore
      
        if (l%1==0):
               print(['iteration '+ str(l+1)+ ' the best fitness is '+ str(gBestScore)]);
    
   
    

    return pos
         
    
def F1(x):
  """ Spere Function """
  s=numpy.sum(x**2);
  return s

def selector(lb,ub,dim,popSize,Iter):
   
    

   
    x=GSA(F1,lb,ub,dim,popSize,Iter)    
    
    return x


# Select general parameters for all optimizers (population size, number of iterations)
PopSize = 80
iterations=500
lb=-100
ub=100
dim=30
func_details=[-100,100,30]

x=selector(lb,ub,dim,PopSize,iterations)
print("the solution of sphere in dim= ",dim," is :",x)