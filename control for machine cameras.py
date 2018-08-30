'''
this script can control machine cameras at the same time
saving data to Q:/test:/``` can change the saving path on line 283 & 286
'''
import PySpin
from multiprocessing import Process
import time
import multiprocessing
"modified from ImageFormat Control"

NUM_IMAGES = 480 * 2      # number of images to grab ()
OFFSET_Y = 800              # the offset of the picture in Y direction
HIGHT = 260                 # the height of the imagines
DELTA = 2                  # take pictures every delta minutes; I do not know what will happen if the time delta is smaller than saving time


def configure_custom_image_settings(nodemap):
    """
    Configures a number of settings on the camera including offsets  X and Y, width,
    height, and pixel format. These settings must be applied before BeginAcquisition()
    is called; otherwise, they will be read only. Also, it is important to note that
    settings are applied immediately. This means if you plan to reduce the width and
    move the x offset accordingly, you need to apply such changes in the appropriate order.

    :param nodemap: GenICam nodemap.
    :type nodemap: INodeMap
    :return: True if successful, False otherwise.
    :rtype: bool
    """
    print '\n*** CONFIGURING CUSTOM IMAGE SETTINGS *** \n'

    try:
        result = True

        # Apply mono 8 pixel format
        #
        # *** NOTES ***
        # Enumeration nodes are slightly more complicated to set than other
        # nodes. This is because setting an enumeration node requires working
        # with two nodes instead of the usual one.
        #
        # As such, there are a number of steps to setting an enumeration node:
        # retrieve the enumeration node from the nodemap, retrieve the desired
        # entry node from the enumeration node, retrieve the integer value from
        # the entry node, and set the new value of the enumeration node with
        # the integer value from the entry node.
        #
        # Retrieve the enumeration node from the nodemap
        node_pixel_format = PySpin.CEnumerationPtr(nodemap.GetNode('PixelFormat'))
        if PySpin.IsAvailable(node_pixel_format) and PySpin.IsWritable(node_pixel_format):

            # Retrieve the desired entry node from the enumeration node
            node_pixel_format_BayerGB8 = PySpin.CEnumEntryPtr(node_pixel_format.GetEntryByName('BayerGB8'))
            if PySpin.IsAvailable(node_pixel_format_BayerGB8) and PySpin.IsReadable(node_pixel_format_BayerGB8):

                # Retrieve the integer value from the entry node
                pixel_format_BayerGB8 = node_pixel_format_BayerGB8.GetValue()

                # Set integer as new value for enumeration node
                node_pixel_format.SetIntValue(pixel_format_BayerGB8)

                print 'Pixel format set to %s...' % node_pixel_format.GetCurrentEntry().GetSymbolic()

            else:
                print 'Pixel format BayerGR 8 not available...'

        else:
            print 'Pixel format not available...'

            # Set maximum width
            #
            # *** NOTES ***
            # Other nodes, such as those corresponding to image width and height,
            # might have an increment other than 1. In these cases, it can be
            # important to check that the desired value is a multiple of the
            # increment. However, as these values are being set to the maximum,
            # there is no reason to check against the increment.
        node_width = PySpin.CIntegerPtr(nodemap.GetNode('Width'))
        if PySpin.IsAvailable(node_width) and PySpin.IsWritable(node_width):

            width_to_set = node_width.GetMax()
            node_width.SetValue(width_to_set)
            print 'Width set to %i...' % node_width.GetValue()

        else:
            print 'Width not available...'

        # Set maximum height
        #
        # *** NOTES ***
        # A maximum is retrieved with the method GetMax(). A node's minimum and
        # maximum should always be a multiple of its increment.
        node_height = PySpin.CIntegerPtr(nodemap.GetNode('Height'))
        if PySpin.IsAvailable(node_height) and PySpin.IsWritable(node_height):

            height_to_set = node_height.GetMax()
            # node_height.SetValue(height_to_set)
            node_height.SetValue(HIGHT)
            print 'Height set to %i...' % node_height.GetValue()

        else:
            print 'Height not available...'

        # Apply minimum to offset X
        #
        # *** NOTES ***
        # Numeric nodes have both a minimum and maximum. A minimum is retrieved
        # with the method GetMin(). Sometimes it can be important to check
        # minimums to ensure that your desired value is within range.
        node_offset_x = PySpin.CIntegerPtr(nodemap.GetNode('OffsetX'))
        if PySpin.IsAvailable(node_offset_x) and PySpin.IsWritable(node_offset_x):

            #node_offset_x.SetValue(node_offset_x.GetMin())
            node_offset_x.SetValue(0)
            print 'Offset X set to %i...' % node_offset_x.GetMin()

        else:
            print 'Offset X not available...'

        # Apply minimum to offset Y
        #
        # *** NOTES ***
        # It is often desirable to check the increment as well. The increment
        # is a number of which a desired value must be a multiple of. Certain
        # nodes, such as those corresponding to offsets X and Y, have an
        # increment of 1, which basically means that any value within range
        # is appropriate. The increment is retrieved with the method GetInc().
        node_offset_y = PySpin.CIntegerPtr(nodemap.GetNode('OffsetY'))
        if PySpin.IsAvailable(node_offset_y) and PySpin.IsWritable(node_offset_y):

            node_offset_y.SetValue(node_offset_y.GetMin()+ OFFSET_Y)
            print 'Offset Y set to %i...' % node_offset_y.GetMin()

        else:
            print 'Offset Y not available...'



    except PySpin.SpinnakerException as ex:
        print 'Error: %s' % ex
        return False

    return result


def print_device_info(nodemap):
    """
    This function prints the device information of the camera from the transport
    layer; please see NodeMapInfo example for more in-depth comments on printing
    device information from the nodemap.

    :param nodemap: Transport layer device nodemap.
    :type nodemap: INodeMap
    :returns: True if successful, False otherwise.
    :rtype: bool
    """

    print '*** DEVICE INFORMATION ***\n'

    try:
        result = True
        node_device_information = PySpin.CCategoryPtr(nodemap.GetNode('DeviceInformation'))

        if PySpin.IsAvailable(node_device_information) and PySpin.IsReadable(node_device_information):
            features = node_device_information.GetFeatures()
            for feature in features:
                node_feature = PySpin.CValuePtr(feature)
                print '%s: %s' % (node_feature.GetName(),
                                  node_feature.ToString() if PySpin.IsReadable(node_feature) else 'Node not readable')

        else:
            print 'Device control information not available.'

    except PySpin.SpinnakerException as ex:
        print 'Error: %s' % ex
        return False

    return result


def acquire_images(start_time, time_delta, cam, nodemap, nodemap_tldevice, index, runtimes):
    data = []
    #start_time = time.time()
    f = open('result.txt','a')
    print '*** IMAGE ACQUISITION ***\n'
    try:
        result = True

        node_acquisition_mode = PySpin.CEnumerationPtr(nodemap.GetNode('AcquisitionMode'))
        if not PySpin.IsAvailable(node_acquisition_mode) or not PySpin.IsWritable(node_acquisition_mode):
            print 'Unable to set acquisition mode to continuous (enum retrieval). Aborting...'
            return False

        # Retrieve entry node from enumeration node
        node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')
        if not PySpin.IsAvailable(node_acquisition_mode_continuous) or not PySpin.IsReadable(
                node_acquisition_mode_continuous):
            print 'Unable to set acquisition mode to continuous (entry retrieval). Aborting...'
            return False

        # Retrieve integer value from entry node
        acquisition_mode_continuous = node_acquisition_mode_continuous.GetValue()

        # Set integer value from entry node as new value of enumeration node
        node_acquisition_mode.SetIntValue(acquisition_mode_continuous)

        #print 'Acquisition mode set to continuous...'

        cam.BeginAcquisition()

        #print 'Acquiring images...'

        device_serial_number = ''
        node_device_serial_number = PySpin.CStringPtr(nodemap_tldevice.GetNode('DeviceSerialNumber'))
        if PySpin.IsAvailable(node_device_serial_number) and PySpin.IsReadable(node_device_serial_number):
            device_serial_number = node_device_serial_number.GetValue()
            print 'Device serial number retrieved as %s...' % device_serial_number




        # Retrieve, convert, and save images
        while ((time.time()-start_time) <= time_delta + 2):
            wait = True
        time1 = time.time()
        print time.time()-start_time
        for i in range(NUM_IMAGES):
            try:

                image_result = cam.GetNextImage()

                if image_result.IsIncomplete():
                    print 'Image incomplete with image status %d ...' % image_result.GetImageStatus(), i

                elif i%4==0:

                    #  Print image information; height and width recorded in pixels
                    #
                    #  *** NOTES ***
                    #  Images have quite a bit of available metadata including
                    #  things such as CRC, image status, and offset values, to
                    #  name a few.


                    ###width = image_result.GetWidth()
                    ###height = image_result.GetHeight()
                    ###print 'Grabbed Image %d, width = %d, height = %d' % (i, width, height)



                    #  Convert image to mono 8
                    #
                    #  *** NOTES ***
                    #  Images can be converted between pixel formats by using
                    #  the appropriate enumeration value. Unlike the original
                    #  image, the converted one does not need to be released as
                    #  it does not affect the camera buffer.
                    #
                    #  When converting images, color processing algorithm is an
                    #  optional parameter.
                    image_converted = image_result.Convert(PySpin.PixelFormat_BayerGB8, PySpin.HQ_LINEAR)
                    data.append(image_converted)
                    image_result.Release()

            except PySpin.SpinnakerException as ex:
                print 'Error: %s' % ex
                return False

        # End acquisition
        #
        #  *** NOTES ***
        #  Ending acquisition appropriately helps ensure that devices clean up
        #  properly and do not need to be power-cycled to maintain integrity.
        # end_time = time.time()
        # delta = start_time - end_time
        # print "delta=", delta
        time2 = time.time()
        f.write('camera:\t' + str(index)+'\n')
        f.write('run time\t' + str(runtimes) + '\n')
        f.write('start time\t' + str(time1)+'\n')

        f.write('end time\t' + str(time2)+'\n')
        f.close()
        for ii in range(len(data)):
            #image_converted = data[ii].Convert(PySpin.PixelFormat_BayerGB8, PySpin.HQ_LINEAR)

            # Create a unique filename
            if device_serial_number:
            #    filename = 'ImageFormatControl-%s-%d.jpg' % (device_serial_number, ii)
                filename = "Q:/test/" + str(index) + '/' + str(runtimes) + '-' + str(ii) + ".jpg"
            else:  # if serial number is empty
            #    filename = 'ImageFormatControl-%d.jpg' % ii
                filename = "Q:/test/" + str(index) + '/' + str(runtimes) + '-' + str(ii) + ".jpe"

            #width = data[ii].GetWidth()
            #height = data[ii].GetHeight()
            if ii%100==0:
                print 'Grabbed Image %d, width = %d, height = %d' % (ii, 2048, 700), filename
            # Save image
            #
            #  *** NOTES ***
            #  The standard practice of the examples is to use device
            #  serial numbers to keep images of one device from
            #  overwriting those of another.
            data[ii].Save(filename)
            # print 'Image saved at %s' % filename

            #  Release image
            #
            #  *** NOTES ***
            #  Images retrieved directly from the camera (i.e. non-converted
            #  images) need to be released in order to keep from filling the
            #  buffer.
            # image_result.Release()
            # print ''
        cam.EndAcquisition()

    except PySpin.SpinnakerException as ex:
        print 'Error: %s' % ex
        return False

    return result


def run_single_camera(index, strat_time):
    system = PySpin.System.GetInstance()

    # Retrieve list of cameras from the system
    cam_list = system.GetCameras()
    cam = cam_list[index]
    print index
    j = 0
    while(True):
        time_now = time.time()
        delta = time_now - strat_time
        time_delta = 3 + 60 * DELTA * j - 2           ###set time per round
        if(delta >= time_delta):
            note = str(index) + '-' + str(j) + '\n'
            try:
                result = True

                # Retrieve TL device nodemap and print device information
                nodemap_tldevice = cam.GetTLDeviceNodeMap()
                note1 = note + '-' + "cam.GetTLDeviceNodeMap()"
                print note1
                result &= print_device_info(nodemap_tldevice)
                note2 = note + '-' + "print_device_info(nodemap_tldevice)"
                print note2
                # Initialize camera
                cam.Init()
                note3 = note + '-' + "cam.Init()"
                print note3
                # Retrieve GenICam nodemap
                nodemap = cam.GetNodeMap()
                note4 = note + '-' + "cam.GetNodeMap()"
                print note4
                # Configure custom image settings
                #if not configure_custom_image_settings(nodemap):
                #    return False
                configure_custom_image_settings(nodemap)
                # Acquire images
                result &= acquire_images(strat_time, time_delta, cam, nodemap, nodemap_tldevice, index, j)

                # Deinitialize camera
                cam.DeInit()

            except PySpin.SpinnakerException as ex:
                print 'Error: %s' % ex
                result = False
            j = j + 1
            #return result


def main():
    result = True

    # Retrieve singleton reference to system object
    system = PySpin.System.GetInstance()

    # Retrieve list of cameras from the system
    cam_list = system.GetCameras()

    num_cameras = cam_list.GetSize()

    print 'Number of cameras detected: %d' % num_cameras

    # Finish if there are no cameras
    if num_cameras == 0:
        # Clear camera list before releasing system
        cam_list.Clear()

        # Release system instance
        system.ReleaseInstance()

        print 'Not enough cameras!'
        raw_input('Done! Press Enter to exit...')
        return False
    start_time = time.time()
    # something added here
    pro = []
    print ("the number of CPU is:" + str(multiprocessing.cpu_count()))
    for i in range(len(cam_list)):
        p = Process(target=run_single_camera, args=(i, start_time,))
        pro.append(p)

    for i in range(len(pro)):
        pro[i].start()

    for pp in multiprocessing.active_children():
        print ("child name:" + pp.name + "id" + str(pp.pid))

    for i in range(len(pro)):
        pro[i].join()


if __name__ == '__main__':
    main()
