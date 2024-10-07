﻿#include <iostream>
#include <random>
#include <algorithm>

typedef struct Room Room;

enum Door {
  NORTH,
  EAST,
  SOUTH,
  WEST,
  UNSET
};

inline Door getSymetric(Door door) {
  switch (door) {
  case NORTH: return SOUTH;
  case EAST:  return WEST;
  case SOUTH: return NORTH;
  case WEST:  return EAST;
  default: return UNSET;
  }
}

struct RoomConnection {
  Room* destRoom;
  Door destDoor;
  bool isParent;

  RoomConnection() : 
    destRoom(nullptr),
    destDoor(UNSET),
    isParent(false) {}
};

#define CONNECTIONS 4
#define FREE_CONNECTIONS 3

struct Room {
  static std::mt19937 rng;
  static std::uniform_int_distribution<int> distribution;

  RoomConnection connections[CONNECTIONS];
  int x;
  int y;

  Room() : x(0), y(0) {}
  ~Room() { destroySubtree(); }


  inline void addParentConnection(Door srcDoor, Room* dstRoom, Door dstDoor) {
    auto& connection = this->connections[srcDoor];
    connection.destRoom = dstRoom;
    connection.destDoor = dstDoor;
    connection.isParent = true;
  }


  inline void addConnection(Door srcDoor, Room* dstRoom, Door dstDoor) {
    auto& connection = this->connections[srcDoor];
    connection.destRoom = dstRoom;
    connection.destDoor = dstDoor;
    connection.isParent = false;
  }


  void generateSubtree(int maxDepth) {
    int door {0};

    // As the root room of the tree, generates 4 rooms and 
    // creates a connection to each of those rooms. Then 
    // generates the corresponding random subtree of rooms.
    //
    // A normal room can have [0-4] connections (including)
    // its parent room connection, but the root room has
    // always 4 connections.

    for(auto& connection : this->connections) {
      Door childDoor {getSymetric((Door)door)};
      Room* child {new Room()};

      child->addParentConnection(childDoor, this, (Door)door);
      this->addConnection((Door)door, child, childDoor);
      
      child->generateSubtree(1, maxDepth);
      ++door;
    }
  }


  void generateSubtree(int depth, int maxDepth) {

    // A non-root room has always one connection used to connect 
    // itself with its parent. The idea here its to get a random 
    // number of unused doors (places to stablish a connection) 
    // and create connection to new rooms. 
    
    Door unusedDoors[FREE_CONNECTIONS] = { UNSET, UNSET, UNSET };
    int doors {0};

    for (int i {0}; i < CONNECTIONS; ++i) {
      if (this->connections[i].destRoom == nullptr) {
        unusedDoors[doors++] = (Door)i;
      }
    }

    const int randConnections {std::min(doors, distribution(rng))};
    if(randConnections == 0) { return; }
    std::shuffle(std::begin(unusedDoors), std::end(unusedDoors), rng);

    for (int i {0}; i < randConnections; ++i) {
      Door iterDoor {unusedDoors[i]};
      Door childDoor {getSymetric(iterDoor)};
      Room* child {new Room()};

      child->addParentConnection(childDoor, this, iterDoor);
      this->addConnection(iterDoor, child, childDoor);

      if((depth + 1) < maxDepth){
        child->generateSubtree(depth + 1, maxDepth);
      }
    }
  } 


  void destroySubtree(void) {
    for (auto& connection : this->connections) {
      if (connection.destRoom != nullptr && !connection.isParent) {
        connection.destRoom->destroySubtree();
        delete connection.destRoom;
        connection.destRoom = nullptr;
      }
    }
  }


  void printSubtree(int depth) {
    std::string fmt;
    int port = 0;

    for (int i = 0; i < depth; i++)
      fmt += "\t";

    std::cout << fmt 
      << "\033[1m\033[32m<@" << (unsigned long long) this
      << ">\033[0m" << std::endl;
       
    for (auto& connection : this->connections) {
      if (connection.destRoom == nullptr) {
        std::cout << fmt
          << "[" << port << "] = @null"
          << std::endl;
      
      } else {
        std::cout << fmt 
          << "[" << port << "] = @"
          << (unsigned long long)connection.destRoom
          << std::endl;
      }
      ++port;
    }

    for (auto& connection : this->connections) {
      if (connection.destRoom != nullptr && !connection.isParent) {
        connection.destRoom->printSubtree(depth + 1);
      }
    }
  }
};

std::mt19937 Room::rng(std::random_device{}());
std::uniform_int_distribution<int> Room::distribution(1, 4);


int main() {
  {
    Room room;
    room.generateSubtree(10);
    room.printSubtree(0);
  }

  return 0;
}
