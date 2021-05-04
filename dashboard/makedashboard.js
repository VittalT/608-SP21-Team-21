rooms = [
    {room_num: "1-115", occupants: 5, capacity: 10},
    {room_num: "1-134", occupants: 0, capacity: 10},
    {room_num: "2-132", occupants: 1, capacity: 10},
    {room_num: "2-151", occupants: 4, capacity: 10},
    {room_num: "2-135", occupants: 8, capacity: 10},
    {room_num: "24-112", occupants: 9, capacity: 10},
    {room_num: "26-142", occupants: 2, capacity: 10},
    {room_num: "32-112", occupants: 5, capacity: 10},
]

const main = () => {
    for(let i = 1; i<=10; i++) {
        makeroom(rooms[i]);
    }
}

main();