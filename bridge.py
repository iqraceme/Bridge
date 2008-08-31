import pygame

class Bridge:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.world = game.world
        self.joints = []
        self.cost = 0

    def create_world(self):
        rect = pygame.Rect((0,800), (350, -250))
        rect.normalize()
        pygame.draw.rect(self.screen, (100,180,255), rect, 3)
        self.world.add.rect(rect.center, rect.width / 2, rect.height / 2,
            dynamic=False)
        rect = pygame.Rect((1200,800), (-350, -250))
        rect.normalize()
        pygame.draw.rect(self.screen, (100,180,255), rect, 3)
        self.world.add.rect(rect.center, rect.width / 2, rect.height / 2,
            dynamic=False)

    def add_cost(self, value):
        self.cost = self.cost + value
        print "cost now", value

    def joint_added(self, joint):
        print "joint added!"
        self.joints.append(joint)
        self.add_cost(100)

    def box_added(self):
        self.add_cost(10)

    def for_each_frame(self):
        for joint in self.joints:
            force = joint.GetReactionForce().Length()
            if force > 500:
                print "destroy joint!"
                self.world.world.DestroyJoint(joint)
                self.joints.remove(joint)

    def create_train(game, worldpoint = (320,500), train = (100, 50), wheelrad = 20, cars = 3):
        points = []
        for i in range(0,cars):
            startpoint = (worldpoint[0]-(train[0]+7)*i, worldpoint[1])
            points.append(startpoint)
            rect = pygame.Rect(startpoint, train)
            rect.normalize()
            pygame.draw.rect(game.screen, (200, 50, 100), rect, 3)
    
            game.world.add.rect(rect.center, rect.width / 2, rect.height / 2,
                dynamic = True, density=10.0, restitution=0.16, friction=0.5)
    
            rearwheel = (startpoint[0]+wheelrad,startpoint[1]+train[1]-wheelrad/2)
            pygame.draw.circle(game.screen, (0,0,0), rearwheel, wheelrad, 3)
            game.world.add.ball(rearwheel,wheelrad, dynamic=True, density=10.0, 
                restitution=0.16, friction=0.5)
    
            frontwheel = (startpoint[0]+train[0]-wheelrad,startpoint[1]+train[1]-wheelrad/2)
            pygame.draw.circle(game.screen, (0,0,0), frontwheel, wheelrad, 3)
            game.world.add.ball(frontwheel,wheelrad, dynamic=True, density=10.0, 
                restitution=0.16, friction=0.5)
    
            rearaxle = game.world.get_bodies_at_pos(rearwheel)
            frontaxle = game.world.get_bodies_at_pos(frontwheel)
            game.world.add.jointMotor(rearaxle[0],rearaxle[1],rearwheel)
            game.world.add.jointMotor(frontaxle[0],frontaxle[1],frontwheel)
            
        for i in range(1,len(points)):
            backlink = (points[i][0]+train[0]-1,points[i][1]+train[1]-1)
            frontlink = (points[i-1][0]+1,points[i-1][1]+train[1]-1)
            btrain = game.world.get_bodies_at_pos(backlink)
            ftrain = game.world.get_bodies_at_pos(frontlink)
            game.world.add.distanceJoint(btrain[0], ftrain[0], backlink, frontlink)
