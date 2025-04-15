planets_default = {
  "planets": [
    {
      "name": "Sun",
      "center": True,
      "size": 40,
      "mass": 10000,
      "speed": 0,
      "children": [
        {
          "name": "A",
          "size": 30,
          "mass": 3000,
          "speed": 15,
          "distanceFromParent": 80,
          "startAngle": 120,
          "children": [
            {
              "name": "A_1",
              "size": 15,
              "mass": 600,
              "speed": 20,
              "distanceFromParent": 40,
              "children": [
              ]
            }
          ]
        },
        {
          "name": "B",
          "size": 25,
          "mass": 3700,
          "speed": 8,
          "distanceFromParent": 145,
          "startAngle": -30,
          "children": [
            {
              "name": "B_1",
              "size": 10,
              "mass": 400,
              "speed": 50,
              "distanceFromParent": 90,
              "children": [
              ]
            },
            {
              "name": "B_2",
              "size": 20,
              "mass": 500,
              "speed": 12,
              "distanceFromParent": 130,
              "children": [
              ]
            }
          ]
        },
        {
          "name": "C",
          "size": 25,
          "mass": 5700,
          "speed": 12,
          "distanceFromParent": 190,
          "startAngle": 90,
          "children": [
            {
              "name": "C_1",
              "size": 15,
              "mass": 1200,
              "speed": 50,
              "distanceFromParent": 40,
              "children": [
              ]
            },
            {
              "name": "C_2",
              "size": 30,
              "mass": 3200,
              "speed": 20,
              "distanceFromParent": 140,
              "children": [
                {
                  "name": "C_2_1",
                  "size": 10,
                  "mass": 450,
                  "speed": 35,
                  "distanceFromParent": 60,
                  "children": [
                  ]
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "name": "Sun2",
      "center": True,
      "position": [700, 1200],
      "size": 40,
      "mass": 12000,
      "speed": 0,
      "children": [
        {
          "name": "A1",
          "size": 30,
          "mass": 300,
          "speed": 15,
          "distanceFromParent": 80,
          "startAngle": -120,
          "children": [
          ]
        },
        {
          "name": "A2",
          "size": 20,
          "mass": 3000,
          "speed": 5,
          "distanceFromParent": 130,
          "startAngle": 340,
          "children": [
            {
              "name": "A2_2",
              "size": 10,
              "mass": 800,
              "speed": 30,
              "distanceFromParent": 40,
              "startAngle": 20,
              "children": [
              ]
            }
          ]
        }
      ]
    }
  ]
}