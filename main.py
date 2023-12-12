import asyncio

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.camera import Camera
from viam.components.board import Board
from viam.components.motor import Motor
from viam.components.base import Base
from viam.components.encoder import Encoder
from viam.components.input import Controller
from viam.services.vision import VisionClient


'''
Our project uses an ml detector to analyze the shape captured by the camera. The 
 confidence threshold is set at 0.45, so if the confidence is greater then 0.45, 
 it will recognize the shape and execute the code to move by following the predesigned 
 track.
'''

async def connect():
    opts = RobotClient.Options.with_api_key(
        api_key='1gi9p9xeskyfbbsr2x33yglrb4klwwec',
        api_key_id='5ceb0675-336b-4e42-8f81-f0835d419f70'
    )
    return await RobotClient.at_address('follower-main.e3zhkh3flg.viam.cloud', opts)

async def moveInSquare(base):
    for _ in range(4):
        await base.move_straight(velocity=500, distance=700)
        await base.spin(velocity=100, angle=90)

async def moveInM(base):
    await base.move_straight(velocity=500, distance=700)
    await base.spin(velocity=100, angle=150)
    await base.move_straight(velocity=500, distance=800)
    await base.spin(velocity=100, angle=-120)
    await base.move_straight(velocity=500, distance=800)
    await base.spin(velocity=100, angle=150)
    await base.move_straight(velocity=500, distance=700)



async def moveInZ(base):
    await base.spin(velocity=100, angle=90)
    await base.move_straight(velocity=500, distance=800)
    await base.spin(velocity=100, angle=-120)
    await base.move_straight(velocity=500, distance=1000)
    await base.spin(velocity=100, angle=120)
    await base.move_straight(velocity=500, distance=800)

async def main():
    robot = await connect()

    print('Resources:')
    # print(robot.resource_names)

    # my-transform-cam
    my_transform_cam = Camera.from_robot(robot, "my-transform-cam")
    my_transform_cam_return_value = await my_transform_cam.get_image()
    print(f"my-transform-cam get_image return value: {my_transform_cam_return_value}")

    # Note that the pin supplied is a placeholder. Please change this to a valid pin you are using.
    # local
    local = Board.from_robot(robot, "local")
    local_return_value = await local.gpio_pin_by_name("16")
    # print(f"local gpio_pin_by_name return value: {local_return_value}")

    # right
    right = Motor.from_robot(robot, "right")
    right_return_value = await right.is_moving()
    # print(f"right is_moving return value: {right_return_value}")

    # left
    left = Motor.from_robot(robot, "left")
    left_return_value = await left.is_moving()
    # print(f"left is_moving return value: {left_return_value}")

    # viam_base
    viam_base = Base.from_robot(robot, "viam_base")
    viam_base_return_value = await viam_base.is_moving()
    # print(f"viam_base is_moving return value: {viam_base_return_value}")

    # cam
    cam = Camera.from_robot(robot, "cam")
    cam_return_value = await cam.get_image()
    # print(f"cam get_image return value: {cam_return_value}")

    # Renc
    renc = Encoder.from_robot(robot, "Renc")
    renc_return_value = await renc.get_position()
    # print(f"Renc get_position return value: {renc_return_value}")

    # Lenc
    lenc = Encoder.from_robot(robot, "Lenc")
    lenc_return_value = await lenc.get_position()
    # print(f"Lenc get_position return value: {lenc_return_value}")

    # WebGamepad
    web_gamepad = Controller.from_robot(robot, "WebGamepad")
    web_gamepad_return_value = await web_gamepad.get_controls()
    # print(f"WebGamepad get_controls return value: {web_gamepad_return_value}")

    # Note that the Camera supplied is a placeholder. Please change this to a valid Camera.
    # vision-model
    vision_model = VisionClient.from_robot(robot, "vision-model")
    vision_model_return_value = await vision_model.get_classifications_from_camera("my-transform-cam", 1)
    print(f"vision-model get_classifications_from_camera return value: {vision_model_return_value}")

    # print(vision_model_return_value.class_name)
    # print(vision_model_return_value.confidence)
    while (True):
        vision_model_return_value = await vision_model.get_classifications_from_camera("my-transform-cam", 1)
        print(vision_model_return_value[0])
        if vision_model_return_value[0].class_name == "square" and vision_model_return_value[0].confidence >= 0.45:
            print("I see a square. Start moving in square shape.")
            await moveInSquare(viam_base)
            await asyncio.sleep(4)
        elif vision_model_return_value[0].class_name == "m" and vision_model_return_value[0].confidence >= 0.45:
            print("I see m shape. Start moving in m shape.")
            await moveInM(viam_base)
            await asyncio.sleep(4)
        elif vision_model_return_value[0].class_name == "z" and vision_model_return_value[0].confidence >= 0.45:
            print("I see z shape. Start moving in z shape.")
            await moveInZ(viam_base)
            await asyncio.sleep(4)
        await asyncio.sleep(0.1)


    # Don't forget to close the robot when you're done!
    await robot.close()


if __name__ == '__main__':
    asyncio.run(main())
