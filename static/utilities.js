// Define our labelmap
const labelMap = {
    1: { name: 'Carrot', color: 'red' },
    2: { name: 'Corn', color: 'yellow' },
    3: { name: 'Dijon_mustard', color: 'lime' },
    4: { name: 'Egg', color: 'blue' },
    5: { name: 'Basil_leaves', color: 'orange' },
    6: { name: 'Honey', color: 'purple' },
    7: { name: 'Balsamic_glaze', color: 'cyan' },
    8: { name: 'Mozzarella', color: 'magenta' },
    9: { name: 'Cheese', color: 'green' },
    10: { name: 'Onion', color: 'pink' },
    11: { name: 'Zucchini', color: 'teal' },
    12: { name: 'Spaghetti', color: 'brown' },
    13: { name: 'Parsley', color: 'violet' },
    14: { name: 'Rice', color: 'navy' },
    15: { name: 'Pasta', color: 'maroon' },
    16: { name: 'Broccoli', color: 'olive' },
    17: { name: 'Milk', color: 'salmon' },
    18: { name: 'Chicken_breast', color: 'skyblue' },
    19: { name: 'Olive_oil', color: 'gold' },
    20: { name: 'Beans', color: 'slategray' },
    21: { name: 'Red_pepper_flakes', color: 'limegreen' },
    22: { name: 'Mushroom', color: 'peru' },
    23: { name: 'Tortillas', color: 'tan' },
    24: { name: 'Lettuce', color: 'khaki' },
    25: { name: 'Garlic', color: 'coral' },
    26: { name: 'Mayonnaise', color: 'orchid' },
    27: { name: 'Tuna', color: 'crimson' },
    28: { name: 'Baguette', color: 'indigo' },
    29: { name: 'Tomatoes', color: 'darkgreen' },
    30: { name: 'Celery', color: 'chocolate' },
    31: { name: 'Bell_pepper', color: 'deeppink' },
    32: { name: 'Ginger', color: 'darkorange' },
    33: { name: 'Soy_sauce', color: 'darkviolet' }
};


// Define a drawing function
export const drawRect = (boxes, classes, scores, threshold, imgWidth, imgHeight, ctx)=>{
    for(let i=0; i<=boxes.length; i++){
        if(boxes[i] && classes[i] && scores[i]>threshold){
            // Extract variables
            const [y,x,height,width] = boxes[i]
            const text = classes[i]
            
            // Set styling
            ctx.strokeStyle = labelMap[text]['color']
            ctx.lineWidth = 10
            ctx.fillStyle = 'white'
            ctx.font = '30px Arial'         
            
            // DRAW!!
            ctx.beginPath()
            ctx.fillText(labelMap[text]['name'] + ' - ' + Math.round(scores[i]*100)/100, x*imgWidth, y*imgHeight-10)
            ctx.rect(x*imgWidth, y*imgHeight, width*imgWidth/2, height*imgHeight/2);
            ctx.stroke()
        }
    }
}