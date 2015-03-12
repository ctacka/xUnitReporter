from xml.etree.ElementTree import Element, ElementTree


class xUnitTestCase(Element):
    def __init__(self, name, time=None, classname=None):
        super(xUnitTestCase, self).__init__('testcase')
        if time and type(time) == type(float): self.set('time', time)
        if classname: self.set('classname', classname)
        self.set('name', name)


    def _add_fail(self, failtype, type, message=None, text=None):
        for el in self: self.remove(el)
        msg = Element(failtype)
        self.append(msg)
        msg.set('type', type)
        if message: msg.set('message', message)
        if text: msg.text = text


    def fail(self, type, message, text=None):
        self._add_fail('failure', type, message, text)

    def error(self, type, message, text=None):
        self._add_fail('error', type, message, text)

    def skip(self, type, text=None):
        self._add_fail('skipped', type, message=None, text)


class xUnitTestSuite(Element):
    def __init__(self, name, hostname=None, timestamp=None):
        super(xUnitReport, self).__init__('testsuite')
        if hostname: self.set('hostname', hostname)
        if timestamp: self.set('timestamp', timestamp)
        self.set('name', name)
        self.recalculate()

    def testcase(self, name, time=None, classname=None):
        tc = xUnitTestCase(name, time, classname)
        self.append(tc)
        return tc


    def recalculate(self):
        failure = 0
        error = 0
        skip = 0
        tests = 0
        time = float(0)
        for tc in self.iter('testcase'):
            tests += 1
            if tc[0].tag == 'failure': failure += 1
            if tc[0].tag == 'error': error += 1
            if tc[0].tag == 'skipped': skip += 1
            time += float(tc.get('time', 0))

        self.set('failures', failure)
        self.set('errors', error)
        self.set('skipped', skip)
        self.set('tests', tests)
        self.set('time', time)


class xUnitReport(Element):
    def __init__(self):
        super(xUnitReport, self).__init__('testsuites')

    def testsuite(self, name, hostname=None, timestamp=None):
        ts = xUnitTestSuite(name, hostname, timestamp)
        self.append(ts)
        return ts

    def dump(self, output):
        for ts in self.iter('testsuite'):
            ts.recalculate()

        ElementTree(self).write(output, encoding='utf-8', xml_declaration=True)
