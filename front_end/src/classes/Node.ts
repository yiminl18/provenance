
  export class Node {

    private id:number 
    private name:string 
    private inNodes:Array<number> = []  
    private outNodes:Array<number> = []
    private inData:Array<number> = []  
    private outData:Array<number> = []
  
    constructor(givenID: number, givenName: string, givenInNodes: Array<number>, 
        givenOutNodes: Array<number>, givenInData: Array<number>, 
        givenOutData: Array<number>) {
      
        this.id = givenID
        this.name = givenName
        this.inNodes = givenInNodes
        this.outNodes = givenOutNodes
        this.inData = givenInData
        this.outData = givenOutData
      
    }


  }

  export default Node
  