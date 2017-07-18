type Course = String
trait Constraint
case class Simple(course: Course) extends Constraint
case class And(constraints: Set[Constraint]) extends Constraint
case class Or(constraints: Set[Constraint]) extends Constraint

def takes(course: Course): Constraint = Simple(course)
def and(c: Constraint*) = And(c.toSet)
def or(c: Constraint*) = Or(c.toSet)

def satisfies(sched: Set[Course], constraint: Constraint): Boolean = constraint match {
  case Simple(course) => sched.contains(course)
  case And(constraints) => 
    constraints.forall(cons => satisfies(sched, cons))
  case Or(constraints) => 
    constraints.exists(cons => satisfies(sched, cons))
}

// courses
val math: Course = "Math"
val physics: Course = "Physics"
val french: Course = "French"

// constraints
val engineering = and(takes(math), takes(physics))
val frenchOrMath = or(takes(french), takes(math))
val complex = and(takes(math), or(takes(physics), takes(french)))

val schedules = List(
  Set(math),
  Set(physics),
  Set(french),
  Set(math, physics),
  Set(math, french),
  Set(physics, french),
  Set(math, physics, french)
)

for(sched <- schedules) {
  println("Schedule " + sched + " satisfies constraints for : ")
  println("engineering :  " + satisfies(sched, engineering))
  println("frenchOrMath : " + satisfies(sched, frenchOrMath))
  println("complex :      " + satisfies(sched, complex))
}