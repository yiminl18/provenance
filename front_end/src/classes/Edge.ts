
export class Edge {

    private inComingId:number 
    private outGoingId:number 
    private relationship:string = "connects to"

  
    constructor(givenInComingid: number, givenOutGoingId: number) {
      
        this.inComingId = givenInComingid
        this.outGoingId = givenOutGoingId     
    }
  }

  export default Edge
  