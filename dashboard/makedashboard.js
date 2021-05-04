
var list = [
    { rn: '1-115', Capacity: 10, nl: 0, vp:0 },
    { rn: '1-134', Capacity: 10, nl: 0, vp:0 },
    { rn: '2-132', Capacity: 10, nl: 0, vp:0 },
    { rn: '2-135', Capacity: 10, nl: 0, vp:0 },
    { rn: '2-151', Capacity: 7, nl: 0, vp:0 },
    { rn: '4-149', Capacity: 10, nl: 0, vp:0 },
    { rn: '4-153', Capacity: 10, nl: 0, vp:0 },
    { rn: '4-167', Capacity: 4, nl: 0, vp:0 },
    { rn: '5-233', Capacity: 10, nl: 0, vp:0 },
    { rn: '8-119', Capacity: 8, nl: 0, vp:0 },
    { rn: '24-112', Capacity: 8, nl: 0, vp:0 },
    { rn: '26-142', Capacity: 8, nl: 0, vp:0 },
    { rn: '32-144', Capacity: 10, nl: 0, vp:0 },
    { rn: '56-154', Capacity: 10, nl: 0, vp:0 },
    { rn: '56-169', Capacity: 8, nl: 0, vp:0 },
    { rn: '66-080', Capacity: 8, nl: 0, vp:0 },
    { rn: 'E51-073', Capacity: 5, nl: 0, vp:0 },
    { rn: 'E53-120', Capacity: 7, nl: 0, vp:0 }
];

const main = () => {
    for(let i = 1; i<=18; i++) {
        makeroom(list[i]);
    }
}

main();