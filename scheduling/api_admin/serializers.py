from rest_framework import serializers

from scheduling.models import Service, Employee, Shift, TimeFrame, Schedule


class ServiceReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class EmployeeReadSerializer(serializers.ModelSerializer):
    services = ServiceReadSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = ('id', 'name', 'first_name', 'last_name', 'instagram',
                  'email', 'phone', 'services', 'profile_img', 'bio')


class EmployeeWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'first_name', 'last_name', 'instagram', 'email', 'phone', 'services', 'profile_img', 'bio')


class TimeFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeFrame
        fields = ('start', 'end')


class ShiftReadSerializer(serializers.ModelSerializer):
    frames = TimeFrameSerializer(many=True, read_only=True, source='timeframe_set')

    class Meta:
        model = Shift
        fields = ('id', 'name', 'frames')


class ShiftWriteSerializer(serializers.ModelSerializer):
    frames = TimeFrameSerializer(many=True, read_only=False, source='timeframe_set')

    class Meta:
        model = Shift
        fields = ('id', 'name', 'frames')

    def create(self, validated_data):
        return updateShift(Shift(), validated_data)

    def update(self, instance, validated_data):
        return updateShift(instance, validated_data)


def updateShift(instance, validated_data):
    instance.name = validated_data['name']
    instance.save()

    frames, validatedFrames = list(instance.timeframe_set.all()), validated_data['timeframe_set']
    instanceLen, validatedLen, = len(frames), len(validatedFrames)

    for i in range(validatedLen if validatedLen > instanceLen else instanceLen):
        # While the shift have frames and there are frames in validated data update them
        if i < instanceLen and i < validatedLen:
            updateFrame(instance, frames[i], validatedFrames[i])
        # When there are extra frames from validated data but none in the shift, create a new frame
        elif i < validatedLen:
            updateFrame(instance, TimeFrame(), validatedFrames[i])
        # Lastly if there are less frames from the update delete the extra frames in the shift
        elif i < instanceLen:
            frame = frames[i]
            frame.delete()

    return instance


def updateFrame(shift, frame, validated_data):
    frame.shift = shift
    frame.start = validated_data['start']
    frame.end = validated_data['end']
    frame.save()


class ScheduleReadSerializer(serializers.ModelSerializer):
    mon, tue, wed, thu, fri, sat, sun = [ShiftReadSerializer(many=False, read_only=True) for i in range(7)]

    class Meta:
        model = Schedule
        fields = ('id', 'name', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')


class ScheduleWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('id', 'name', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')
