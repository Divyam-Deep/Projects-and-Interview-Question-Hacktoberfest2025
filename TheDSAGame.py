




import random
"""
TheDSAGame - Docstring / Game Overview

This module implements a small terminal-based puzzle / stealth game that
combines graph algorithms, pathfinding, and resource management. The playfield
is a rectangular grid of nodes (cells) connected by undirected edges with
integer weights. The player must navigate from a start cell to an exit cell
while managing limited energy, toggling edges (links) to form a connected
network, and avoiding moving guards. Some edges are marked as "critical" and
belong to a minimum spanning tree (MST) computed at startup; activating these
is necessary to ensure the network between the player and the exit can be
connected.

Key concepts and components
- Grid graph:
    - Nodes correspond to grid cells (rows x cols).
    - Edges exist between orthogonally adjacent cells and have a random weight.
    - Edges can be active or inactive; active edges are traversable by the
        player and influence guard movement costs.

- DSU (Disjoint Set Union / Union-Find):
    - Used to compute connectivity when determining the MST (Kruskal's
        algorithm) and to check active connectivity between the player's node and
        the exit node.

- Kruskal's algorithm:
    - Computes an MST on the full grid graph by sorting edges by weight and
        unioning components using the DSU structure. Edges in the MST are marked
        as "critical".

- Edge states:
    - active: whether the edge is currently open/traversable.
    - critical: whether the edge belongs to the MST (important edges the player
        should prioritize activating).

- Player and exit:
    - The player starts at cell 0 (top-left).
    - The exit is at the last cell (bottom-right).
    - Player movement is restricted to neighboring cells and only allowed across
        active edges.

- Guards (enemies):
    - A small set of guard agents are placed randomly on the grid.
    - Each turn, guards compute shortest-path distances from their current
        position using Dijkstra's algorithm over the graph where active edges
        have lower traversal cost and inactive edges have a higher traversal cost.
    - Guards greedily move to neighboring cells that reduce their computed
        distance to the player's current cell. Guards capture the player if they
        occupy the same cell.

- Pathfinding (Dijkstra):
    - Used by guards to compute distances respecting active/inactive edge
        traversal costs. Active edges are cheap; inactive edges are expensive,
        so guards prefer to use active links.

Gameplay and mechanics
- Turn-based loop:
    - Each loop iteration represents one turn. The player issues a command,
        then guards move, and energy is decremented.

- Commands:
    - Movement: w/a/s/d or up/left/down/right to attempt to move into an
        adjacent cell. Movement only succeeds if the corresponding edge is active.
    - Toggle edge: 't' to toggle an adjacent edge's active state. The player
        is prompted for a direction (u/d/l/r or WASD variants). Toggling an edge
        costs energy.
    - Quit: 'q' to exit the game.

- Energy:
    - The player starts with a finite amount of energy (a resource).
    - Certain actions consume energy (toggling edges costs energy; each turn
        also reduces energy). Running out of energy results in failure.

- Victory and defeat:
    - Victory: reach the exit cell while the player's connected component (over
        active edges) contains the exit — i.e., the network is connected from the
        player to the exit.
    - Defeat: be captured by a guard (occupying the same cell) or run out of
        energy.
    - The game also displays the count of "critical" MST edges that remain
        inactive to encourage the player to prioritize their activation.

Rendering and UI
- Terminal-based rendering prints a 2D textual view of the grid where:
    - '.' is an empty cell or inactive edge,
    - '-' or '|' indicates active horizontal/vertical edges,
    - special characters indicate critical inactive edges differently,
    - 'P' represents the player, 'X' the exit, 'G' guards, and '!' a clash
        marker when a guard shares the player's cell.
- A legend and status line show current turn, remaining energy, and how to
    control the game.

Implementation notes and algorithms
- The grid graph is represented by an edge dictionary keyed by frozenset({a,b})
    where a and b are node indices. This makes edges undirected and easy to
    lookup and toggle.
- MST computation uses Kruskal's algorithm with an in-house DSU class.
- Guards use Dijkstra's algorithm on a weighted graph where the cost to cross
    an edge depends only on whether it is active (low cost) or inactive (high
    cost).
- Active connectivity between two nodes is computed by running a DSU over
    currently active edges and comparing roots.

Potential improvements
- More informative rendering (show edge weights, clearer critical edge
    symbols).
- Better guard AI (e.g., multi-step planning or coordination).
- Save/load game state, difficulty levels, procedurally generated objectives,
    or multiple levels.
- Refactor rendering code to remove repeated calculations and simplify grid
    coordinate mapping.
- Replace blocking input with a non-blocking or GUI interface for better UX.

"""
import heapq
import os
import sys

random.seed()

class DSU:
    def __init__(self,n):
        self.p=list(range(n))
    def find(self,a):
        while self.p[a]!=a:
            self.p[a]=self.p[self.p[a]]
            a=self.p[a]
        return a
    def union(self,a,b):
        ra,rb=self.find(a),self.find(b)
        if ra==rb: return False
        self.p[rb]=ra
        return True

class Edge:
    def __init__(self,a,b,w):
        self.a=a
        self.b=b
        self.w=w
        self.active=False
        self.critical=False

def idx(r,c,cols):
    return r*cols+c

def neighbors(r,c,rows,cols):
    for dr,dc in ((0,1),(1,0),(-1,0),(0,-1)):
        nr,nc=r+dr,c+dc
        if 0<=nr<rows and 0<=nc<cols:
            yield nr,nc

def build_grid(rows,cols):
    edges={}
    for r in range(rows):
        for c in range(cols):
            for nr,nc in neighbors(r,c,rows,cols):
                if (r,c)<(nr,nc):
                    a=idx(r,c,cols); b=idx(nr,nc,cols)
                    w=random.randint(1,9)
                    edges[frozenset((a,b))]=Edge(a,b,w)
    return edges

def kruskal(edges,n):
    items=list(edges.items())
    items.sort(key=lambda kv:kv[1].w)
    dsu=DSU(n)
    mst=[]
    for k,e in items:
        if dsu.union(e.a,e.b):
            mst.append(k)
    return set(mst)

def active_connectivity(edges,n):
    dsu=DSU(n)
    for k,e in edges.items():
        if e.active:
            dsu.union(e.a,e.b)
    return dsu

def dijkstra(edges,rows,cols,source):
    n=rows*cols
    dist=[10**9]*n
    dist[source]=0
    pq=[(0,source)]
    adj={}
    for k,e in edges.items():
        adj.setdefault(e.a,[]).append((e.b,1 if e.active else 5))
        adj.setdefault(e.b,[]).append((e.a,1 if e.active else 5))
    while pq:
        d,u=heapq.heappop(pq)
        if d!=dist[u]: continue
        for v,w in adj.get(u,[]):
            nd=d+w
            if nd<dist[v]:
                dist[v]=nd
                heapq.heappush(pq,(nd,v))
    return dist

def clear():
    os.system('cls' if os.name=='nt' else 'clear')

def render(rows,cols,edges,player,guards,exit_pos,turn,energy):
    grid=[['.' for _ in range(cols*2-1)] for __ in range(rows*2-1)]
    for r in range(rows):
        for c in range(cols):
            gr, gc = r*2, c*2
            grid[gr][gc]='.'
    for k,e in edges.items():
        a=e.a; b=e.b
        ar,ac=divmod(a,cols); br,bc=divmod(b,cols)
        mr,my = ar+br, ac+bc
        gr, gc = mr, my
        gr//=1; gc//=1
        gr*=1; gc*=1
        gr = ar+br; gc = ac+bc
        gr//=2; gc//=2
        gr*=1; gc*=1
        gr=ar+br; gc=ac+bc
        gr//=2; gc//=2
        gr*=1; gc*=1
        gr*=1; gc*=1
        posr = ar+br
        posc = ac+bc
        posr//=2; posc//=2
        gi = posr*2; gj = posc*2
        if ar==br:
            ch='-' if e.active else ('=' if e.critical else '.')
            grid[gi][gj]=ch
        else:
            ch='|' if e.active else ('!' if e.critical else '.')
            grid[gi][gj]=ch
    plr,plc=divmod(player,cols)
    exr,exc=divmod(exit_pos,cols)
    grid[plr*2][plc*2]='P'
    grid[exr*2][exc*2]='X'
    for i,g in enumerate(guards):
        gr, gc = divmod(g,cols)
        if grid[gr*2][gc*2]=='P':
            grid[gr*2][gc*2]='!'
        else:
            grid[gr*2][gc*2]='G'
    print("Turn:",turn,"Energy:",energy,"(t to toggle edge, wasd to move, q quit)")
    print("Legend: P=you X=exit G=guard - active edge | active edge !/=/! critical inactive")
    for row in grid:
        print(''.join(row))

def adjacent_nodes(node,rows,cols):
    r,c=divmod(node,cols)
    for nr,nc in neighbors(r,c,rows,cols):
        yield idx(nr,nc,cols)

def toggle_edge(edges,a,b):
    key=frozenset((a,b))
    if key in edges:
        edges[key].active=not edges[key].active
        return True
    return False

def guards_move(edges,rows,cols,guards,player):
    new=[]
    for g in guards:
        dist=dijkstra(edges,rows,cols,g)
        next_node=g
        best=None
        for nb in adjacent_nodes(g,rows,cols):
            if dist[nb]<dist[g]:
                if best is None or dist[nb]<dist[best]:
                    best=nb
        if best is None:
            pass
        else:
            next_node=best
        new.append(next_node)
    return new

def main():
    rows,cols=6,6
    n=rows*cols
    edges=build_grid(rows,cols)
    mst=kruskal(edges,n)
    for k in mst:
        edges[k].critical=True
    for k,e in edges.items():
        e.active=random.random()<0.25 or e.critical and random.random()<0.5
    player=0
    exit_pos=n-1
    guards=[random.randint(0,n-1) for _ in range(3)]
    turn=0
    energy=40
    while True:
        clear()
        render(rows,cols,edges,player,guards,exit_pos,turn,energy)
        dsu=active_connectivity(edges,n)
        connected = dsu.find(player)==dsu.find(exit_pos)
        crit_left=sum(1 for k in mst if not edges[k].active)
        print("Critical edges remaining to activate:",crit_left)
        if player==exit_pos and connected:
            print("CONGRATULATIONS! You reached the exit with network connected.")
            break
        elif player in guards:
            print("CAPTURED! A guard caught you.")
            break
        if energy<=0:
            print("OUT OF ENERGY! You failed to finish.")
            break
        cmd=input("cmd: ").strip().lower()
        turn+=1
        if cmd=='q':
            print("Goodbye")
            break
        if cmd=='t':
            try:
                rc=input("toggle direction (u/d/l/r): ").strip().lower()
            except:
                rc=''
            r,c=divmod(player,cols)
            target=None
            if rc in ('u','w'):
                nr,nc=r-1,c
            elif rc in ('d','s'):
                nr,nc=r+1,c
            elif rc in ('l','a'):
                nr,nc=r,c-1
            elif rc in ('r','d','e'):
                nr,nc=r,c+1
            else:
                nr,nc=None,None
            if nr is None or not (0<=nr<rows and 0<=nc<cols):
                print("No edge there")
            else:
                a=player; b=idx(nr,nc,cols)
                if toggle_edge(edges,a,b):
                    energy-=2
                else:
                    print("Not toggleable")
        elif cmd in ('w','a','s','d','up','left','down','right'):
            r,c=divmod(player,cols)
            if cmd in ('w','up'):
                nr,nc=r-1,c
            elif cmd in ('s','down'):
                nr,nc=r+1,c
            elif cmd in ('a','left'):
                nr,nc=r,c-1
            elif cmd in ('d','right'):
                nr,nc=r,c+1
            else:
                nr,nc=None,None
            if nr is None or not (0<=nr<rows and 0<=nc<cols):
                pass
            else:
                a=player; b=idx(nr,nc,cols)
                key=frozenset((a,b))
                if key in edges and edges[key].active:
                    player=b
                else:
                    print("Edge inactive. Use toggle to activate.")
        else:
            print("Unknown command")
        guards = guards_move(edges,rows,cols,guards,player)
        energy-=1

if __name__=='__main__':
    main()