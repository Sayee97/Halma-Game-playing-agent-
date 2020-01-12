import math
import time
import sys
import copy
import sys
start_time = time.time()
class TreeNode:
	terrain=[]
	val=0
	children=None
	nodeType=0
	destination=[]
	source=[]
	depth=0
	colorPlayer=""
	possiblebache=[]
	def __init__(self,terrain,val,children,nodeType,source,colorPlayer,depth,destination,possiblebache):
		self.terrain=terrain
		self.val=val
		self.children=children
		self.nodeType=nodeType
		self.source=source
		self.destination=destination
		self.colorPlayer=colorPlayer
		self.depth=depth
		self.possiblebache=possiblebache

file1 = open("input.txt","r+")
fileOutput=open("output.txt","w+")
game=file1.readline().strip()
color=file1.readline().strip()
t=file1.readline().strip()
terrain=[]
res=[]
for i in range(16):
	q=file1.readline().strip()
	res=[]
	for i in q:
		res.append(i)
	terrain.append(res)
if game=="SINGLE":
	depthDefined=1
elif game=="GAME":
	if float(t)<5.0:
		depthDefined=1
	else:
		depthDefined=3

goalBlack=[[0,0],[1,0],[2,0],[3,0],[4,0],
			[0,1],[1,1],[2,1],[3,1],[4,1],
			[0,2],[1,2],[2,2],[3,2],
			[0,3],[1,3],[2,3],
			[0,4],[1,4]]
goalWhite=[[14,11],[15,11],
			[13,12],[14,12],[15,12],
			[12,13],[13,13],[14,13],[15,13],
			[11,14],[12,14],[13,14],[14,14],[15,14],
			[11,15],[12,15],[13,15],[14,15],[15,15]]


goalBlack1=[str([0,0]),str([1,0]),str([2,0]),str([3,0]),str([4,0]),
			str([0,1]),str([1,1]),str([2,1]),str([3,1]),str([4,1]),
			str([0,2]),str([1,2]),str([2,2]),str([3,2]),
			str([0,3]),str([1,3]),str([2,3]),
			str([0,4]),str([1,4])]

goalWhite1=[str([14,11]),str([15,11]),
			str([13,12]),str([14,12]),str([15,12]),
			str([12,13]),str([13,13]),str([14,13]),str([15,13]),
			str([11,14]),str([12,14]),str([13,14]),str([14,14]),str([15,14]),
			str([11,15]),str([12,15]),str([13,15]),str([14,15]),str([15,15])]

   

def checkNeighbours(x,y,goal,terrain,winningGoal):
	s=""
	validMoves=[]
	
	possiblititiesR=[1,1,1,0,0,-1,-1,-1]
	possibilitiesC=[1,0,-1,1,-1,1,0,-1]

	jumps=jumpInfi(x,y,[],goal,terrain)
	validMoves.extend(jumps)
	for i in range(8):
		xChild=x+possiblititiesR[i]
		yChild=y+possibilitiesC[i]

		if isValidNeighbour(xChild,yChild, goal,terrain):

			validMoves.append([xChild,yChild])
		if [yChild,xChild] in goal:

			if isValidNeighbourHome(x,y,xChild,yChild,terrain):
				validMoves.append([xChild,yChild])


		if [yChild,xChild] in winningGoal and [y,x] in winningGoal:
			if isValidDestination(x,y,xChild,yChild,terrain):
				validMoves.append([xChild,yChild])


	return validMoves

def jumpInfi(x,y,prevSpots,goal,terrain):
	possiblititiesR=[1,1,1,0,0,-1,-1,-1]
	possibilitiesC=[1,0,-1,1,-1,1,0,-1]

	jumps=[]
	i=0
	for i in range(8):
		xChild=x+possiblititiesR[i]
		yChild=y+possibilitiesC[i]
		if xChild>=0 and xChild<=15 and yChild>=0 and yChild<=15:
			if terrain[yChild][xChild]!='.':
				m=x+(possiblititiesR[i]*2)
				n=y+(possibilitiesC[i]*2)
				if m>=0 and m<=15 and n>=0 and n<=15:
					if terrain[n][m]=='.'  and [m,n] not in prevSpots: #and [n,m] not in goal
						jumps.append([m,n])
						prevSpots.append([x,y])
						future_hops=jumpInfi(m,n,prevSpots,goal,terrain)

						jumps.extend(future_hops)
	return jumps
def isValidNeighbour(xChild,yChild, goal,terrain):
	if goal==goalWhite:
		g=goalWhite1
	elif goal==goalBlack:
		g=goalBlack1
	if xChild>=0 and xChild<=15 and yChild>=0 and yChild<=15:
	 	s="["+str(yChild)+", "+str(xChild)+"]"
	 	if terrain[yChild][xChild]=='.' and s not in g:
	 		return True

def isValidNeighbourHome(x,y,xChild,yChild,terrain):

	if terrain[y][x]=='W' and abs(x-15)+abs(y-15)<abs(xChild-15)+abs(yChild-15) and terrain[yChild][xChild]==".":
		return True
	elif terrain[y][x]=='B' and abs(x-0)+abs(y-0)<abs(xChild-0)+abs(yChild-0) and terrain[yChild][xChild]==".":
		return True
def isValidDestination(x,y,xChild,yChild,terrain):


	if terrain[y][x]=="B" and abs(x-15)+abs(y-15)>abs(xChild-15)+abs(yChild-15) and terrain[yChild][xChild]==".":
		return True
	elif terrain[y][x]=='W' and abs(x-0)+abs(y-0)>abs(xChild-0)+abs(yChild-0) and terrain[yChild][xChild]==".":
		return True

def hypotenuseDistance(point1X,point1Y,point2X,point2Y):
	return math.sqrt((point1X-point2X)**2 + (point2Y-point1Y)**2)

def utility(Node):
	black=0
	white=0

	for i in range(16):
		for j in range(16):
			
			if Node.terrain[j][i]=="W":
				s="["+str(Node.destination[1])+", "+str(Node.destination[0])+"]"

				d=[]
				winningGoal=goalBlack
				wg=goalBlack1
				for g in winningGoal:
					if Node.terrain[g[1]][g[0]]!="W":
						d.append(hypotenuseDistance(i,j,g[1],g[0]))

				if len(d):
					white+=max(d)
				elif s  in wg  and [Node.source[1],Node.source[0]] in goalWhite:
					white=2**-31
				else:
					white=-500
			if Node.terrain[j][i]=="B":
				s="["+str(Node.destination[1])+", "+str(Node.destination[0])+"]"

				d=[]
				winningGoal=goalWhite
				wg=goalWhite1
				for g in winningGoal:
					if Node.terrain[g[1]][g[0]]!="B":
						d.append(hypotenuseDistance(i,j,g[1],g[0]))

				if len(d):
					black+=max(d)
				elif s in wg and [Node.source[1],Node.source[0]] in goalBlack:
					black=2*-31

				else:
					black=-500

	if Node.colorPlayer=="B":

		utilValue= black/white
	elif Node.colorPlayer=="W":

		utilValue=white/black

	return utilValue


def createChildren(Node):

	p=[]
	pGhar=[]

	c=Node.colorPlayer
	u=Node.nodeType

	if u==0:
		childVal=2**31-1
		childType=1
	elif u==1:
		childVal=-2**31
		childType=0

	if c=="B":
		childColorPlayer="W"
		winningGoal=goalWhite
		wg=goalWhite1
		goal=goalBlack
		g=goalBlack1
	elif c=="W":
		winningGoal=goalBlack
		goal=goalWhite
		wg=goalBlack1
		g=goalWhite1
		childColorPlayer="B"

	#if Node.depth==0:

	p=[]
	pGhar=[]
	p=[[j,i] for i in range(16) for j in range(16) if Node.terrain[j][i]==c and ("["+str(j)+", "+str(i)+"]") not in g] 
	pGhar=[[j,i] for i in range(16) for j in range(16) if Node.terrain[j][i]==c and ("["+str(j)+", "+str(i)+"]") in g] 

	i=0
	while(i<len(pGhar)):
		xCoordinate=pGhar[i][1]
		yCoordinate=pGhar[i][0]
		s="["+str(yCoordinate)+", "+str(xCoordinate)+"]"

		if s not in wg:
			possibleMoves=checkNeighbours(xCoordinate,yCoordinate,goal,Node.terrain,winningGoal)

			#print(possibleMoves)

			for j in possibleMoves:

				modBoard= copy.deepcopy(Node.terrain)
				l=TreeNode(modBoard,childVal,[],childType,[xCoordinate,yCoordinate],childColorPlayer,Node.depth+1,[j[0],j[1]],possibleMoves)
				l.terrain[yCoordinate][xCoordinate]="."
				l.terrain[j[1]][j[0]]=c
				l.possiblebache=possibleMoves
				l.childColorPlayer=childColorPlayer

				Node.children.append(l)




		i=i+1
	if len(Node.children)>0:
		return Node.children

	else:
		i=0
		while(i<len(p)):
			xCoordinate=p[i][1]
			yCoordinate=p[i][0]
			s="["+str(yCoordinate)+", "+str(xCoordinate)+"]"

			if s not in wg:
				possibleMoves=checkNeighbours(xCoordinate,yCoordinate,goal,Node.terrain,winningGoal)

				for j in possibleMoves:

					modBoard= copy.deepcopy(Node.terrain)
					l=TreeNode(modBoard,childVal,[],childType,[xCoordinate,yCoordinate],childColorPlayer,Node.depth+1,[j[0],j[1]],possibleMoves)
					l.terrain[yCoordinate][xCoordinate]="."
					l.terrain[j[1]][j[0]]=c
					l.possiblebache=possibleMoves
					l.childColorPlayer=childColorPlayer

					Node.children.append(l)

			elif s in wg:
				possibleMoves=checkNeighbours(xCoordinate,yCoordinate,goal,Node.terrain,winningGoal)

				for j in possibleMoves:

					modBoard= copy.deepcopy(Node.terrain)
					l=TreeNode(modBoard,childVal,[],childType,[xCoordinate,yCoordinate],childColorPlayer,Node.depth+1,[j[0],j[1]],possibleMoves)
					l.terrain[yCoordinate][xCoordinate]="."
					l.terrain[j[1]][j[0]]=c
					l.possiblebache=possibleMoves
					l.childColorPlayer=childColorPlayer

					Node.children.append(l)
			i=i+1
		return Node.children


def alphabeta(Node):
	v=max_value(Node,-2**31,2**31-1)
	for i in Node.children:
		if i.val==v:
			print("heyyyyyy")
			return i
def max_value(Node, alpha, beta):
	global depthDefined
	if Node.colorPlayer=="B":
		winningGoal=goalBlack
		wg=goalBlack1
	else:
		winningGoal=goalWhite
		wg=goalWhite1
	s="["+str(Node.destination[1])+", "+str(Node.destination[0])+"]"
	if Node.depth==depthDefined:
		Node.val=utility(Node)
		return Node.val
	else:
		v=-2**31

		Node.children=createChildren(Node)

		if Node.depth==0 and len(Node.children)>60:
			depthDefined=1
		
		for child in Node.children:
			v=max(v,min_value(child,alpha,beta))
			if v>=beta:
				Node.val=v
				return v
			alpha=max(alpha,v)

		Node.val=v
		return v

def min_value(Node, alpha, beta):





	s="["+str(Node.destination[1])+", "+str(Node.destination[0])+"]"

	s1="["+str(Node.source[1])+", "+str(Node.source[0])+"]"
	if Node.depth==depthDefined:

		Node.val=utility(Node)
		return Node.val
	else:
		v=2**31-1
		Node.children=createChildren(Node)



		for child in Node.children:

			v=min(v,max_value(child,alpha,beta))


			if Node.depth==1:


				if child.colorPlayer=="B" and (s1 in goalBlack1 and s not in goalBlack1):

					v=v*1000
					print(s,"ja bhai",v)
					break
				elif child.colorPlayer=='W' and (s1  in goalWhite1 and s not in goalWhite1):

					v=v*1000
					print(s,"ja bhai",v)
					break

				if child.colorPlayer=='B' and (s in goalBlack1 and s1 in goalBlack1):

					v=v*700
					print(s,"yuhuuuu",v)

				elif child.colorPlayer=='W' and (s in goalWhite1 and s1 in goalWhite1):

					v=v*700
					print("yuhuuu")

				if child.colorPlayer=='W' and (s in goalBlack1 and s1 not in goalBlack1):

					v=v*500
					print("yuhuuu")
				elif child.colorPlayer=='B' and (s in goalWhite1 and s1 not in goalWhite1):

					v=v*500
					print("bakwas")

				if child.colorPlayer=="B" and (s in goalWhite1 and s1 in goalWhite1):
	
					v=v*200
					print("bakwas")
				elif child.colorPlayer=="W" and (s in goalBlack1 and s1 in goalBlack1):

					v=v*200
					print("bakwas")



			if v<=alpha:

				Node.val=v
				return v
			beta=min(beta,v)

		Node.val=v	
		return v


def printPath(kids,src,dest,Node):
	kids.insert(0,src)
	inde=kids.index([dest[0],dest[1]])
	ans=kids[0:inde+1]
	ans2=[]
	l=ans[::-1]
	i=0
	while(i<len(l)-1):

		p=l[i+1][0]-l[i][0]
		q=l[i+1][1]-l[i][1]

		if abs(p)==2 and abs(q)==2:



			r=l[i][0]+(l[i+1][0]-l[i][0])//2
			s=l[i][1]+(l[i+1][1]-l[i][1])//2


			if terrain[s][r]!='.':
				ans2.append([l[i][0],l[i][1]])
				i=i+1
			else:
				l.remove([l[i+1][0],l[i+1][1]])
		else:
			l.remove([l[i+1][0],l[i+1][1]])
	ans2.append(src)
	ans2.reverse()
	return ans2

def structure():
	xCoordinate=None
	yCoordinate=None
	goal=""
	count=0
	col=""
	pawns=[]
	winningGoal=""
	if color=="WHITE":
		col="W"
		goal=goalWhite
		winningGoal=goalBlack
	if color=="BLACK":
		col="B"
		goal=goalBlack
		winningGoal=goalWhite

	TreeRoot=TreeNode(terrain,-2**31,[],1,[0,0],col,0,[-1,-1],[])

	i=alphabeta(TreeRoot)
	print("Source",i.source)
	print("Destination",i.destination)


	if abs(i.source[0]-i.destination[0]) >1 or abs(i.source[1]-i.destination[1])>1:
		listAns=printPath(i.possiblebache,i.source,i.destination,i)
		ans=""
		for i in range(len(listAns)-1):
			p="J "+str(listAns[i][0])+","+str(listAns[i][1])+" "+str(listAns[i+1][0])+","+str(listAns[i+1][1])+"\n"
			ans=ans+p
		ans=ans.strip()
		print(ans)
		finalAns=""
		finalAns=ans
		#wer="sayee chutya"
		fileOutput.write(finalAns)
		fileOutput.close()

	else:
		p="E "+str(i.source[0])+","+str(i.source[1])+" "+str(i.destination[0])+","+str(i.destination[1])
		print(p)
		#wer="sayee chutya"
		finalAns=p
		#fileOutput.write("heyyyy")
		fileOutput.write(finalAns)
		fileOutput.close()

def single():
	structure()
def game1():
	structure()

def main():

	s=str(game)
	if game=="SINGLE":
		single()
	if game=="GAME":
		game1()	
if __name__ == "__main__":
    main()
    print("--- %s seconds ---" % (time.time() - start_time))

   	








