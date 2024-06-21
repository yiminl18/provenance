
  export class Node {

    private id:number 
    private name:string 
    private inNodes:Array<number> = []  
    private outNodes:Array<number> = []
    private inData:Array<string> = []  
    private outData:Array<string> = []
    private correctedInData:Array<any> = []
  
    constructor(givenID: number, givenName: string, givenInNodes: Array<number>, 
        givenOutNodes: Array<number>, givenInData: Array<string>, 
        givenOutData: Array<string>) {
      
        this.id = givenID
        this.name = givenName
        this.inNodes = givenInNodes
        this.outNodes = givenOutNodes
        this.inData = givenInData
        this.outData = givenOutData

    }

    formatDataWithNewlines(StringtoBeChanged: string){
      var newData = StringtoBeChanged.replace(/\n/g, '<br />')
      return newData;

    }



    // formatDataWithNewlines2() {
    //   this.inData.map((data, index)=>
    //     this.correctedInData.push(this.formatDataWithNewlines(data))
    //   )
    // }

  }

  export default Node
  