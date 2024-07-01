
  export class Node {

    private id:number 
    private name:string 
    private inNodes:Array<number> = []  
    private outNodes:Array<number> = []
    private inData:Array<string> = []  
    private outData:Array<string> = []
    private label:string
    private prompt:string
  
    constructor(givenID: number, givenName: string, givenInNodes: Array<number>, 
        givenOutNodes: Array<number>, givenInData: Array<string>, 
        givenOutData: Array<string>, givenLabel: string, givenPrompt: string) {
      
        this.id = givenID
        this.name = givenName
        this.inNodes = givenInNodes
        this.outNodes = givenOutNodes
        this.inData = givenInData
        this.outData = givenOutData
        this.label = givenLabel
        this.prompt = givenPrompt

    }

    formatDataWithNewlines(StringtoBeChanged: string){
      var newData = StringtoBeChanged.replace(/\n/g, '<br />')
      return newData;

    }

  }

  export default Node
  