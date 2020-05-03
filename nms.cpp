#include <iostream>
#include <opencv2/opencv.hpp>
#include <assert.h>
#include <algorithm>
using namespace std;
using namespace cv;

//nms for all the boxes in one test image
//boxes: the all boxes predicted in one image
//scores: the scores of the boxes predicted of one image
//threshold: IoU threshold to use for filtering.
typedef struct BOX{
    BOX(int _x1,int _y1,int _x2,int _y2){
        this->x1 = _x1;
        this->x2 = _x2;
        this->y1 = _y1;
        this->y2 = _y2;
    }
    BOX(int x,int y,int w,int h,int){
        this->x1 = x-w/2;
        this->x2 = x+w/2;
        this->y1 = y-h/2;
        this->y2 = y+h/2;
    }
    int x1;
    int x2;
    int y1;
    int y2;
}BOX;
template <typename T>
vector<int> argsort(const vector<T>& array,bool rever=true)
{
    const int array_len(array.size());
    vector<int> array_index(array_len, 0);
    for (int i = 0; i < array_len; ++i)
        array_index[i] = i;

    sort(array_index.begin(), array_index.end(),
              [&array](int pos1, int pos2) {return (array[pos1] < array[pos2]);});
    if(rever) {
        reverse(array_index.begin(),array_index.end());
    }
    return array_index;
}

class NMS{
public:
    vector<int> after_NMS(const vector<BOX> boxes,vector<double> scores,double threshold){
        assert(boxes.size()>0);
        vector<double> area;
        for(int i=0;i<boxes.size();i++){
            BOX b = boxes[i];
            area.push_back((boxes[i].y2-boxes[i].y1)*(boxes[i].x2-boxes[i].x1));
        }
        vector<int> ixs = argsort<double>(scores);
        vector<int> pick;
        while (!ixs.empty()){
            int i = ixs[0];
            pick.push_back(i);
            doNms(boxes,area,ixs,threshold);

        }
        return pick;
    }
    void doNms(const vector<BOX> boxes,const vector<double> boxes_area,vector<int>& ixs,double threshold=0.8){
        int idx = ixs[0];
        ixs.erase(ixs.begin());
        for(vector<int>::iterator it = ixs.begin();it!=ixs.end();){
            int x1 = max(boxes[idx].x1,boxes[*it].x1);
            int y1 = max(boxes[idx].y1,boxes [*it].y1);
            int x2 = min(boxes[idx].x2,boxes[*it].x2);
            int y2 = min(boxes[idx].y2,boxes[*it].y2);
            double intersection_ = max(x2-x1,0)*max(y2-y1,0);
            double union_ = boxes_area[idx]+boxes_area[*it]-intersection_;
            double iou = intersection_/union_;
            if(iou>threshold){
                ixs.erase(it);//删除元素，返回值指向已删除元素的下一个位置
            }
            else{
                it++;
            }
        }
    }
};


int main() {
    std::cout << "Hello, World!" << std::endl;
    vector<BOX> boxes;
    boxes.push_back(BOX(63,63,127,127));
    boxes.push_back(BOX(383,63,447,127));
    boxes.push_back(BOX(63,383,127,447));
    boxes.push_back(BOX(383,383,447,447));
    boxes.push_back(BOX(255,255,319,319));

    boxes.push_back(BOX(73,53,127,127));
    boxes.push_back(BOX(373,63,447,127));
    boxes.push_back(BOX(73,383,127,457));
    boxes.push_back(BOX(367,383,441,457));
    boxes.push_back(BOX(265,245,309,329));
    vector<double> scores = {1.0,0.96,0.99,0.87,0.90,0.90,0.89,0.92,0.77,0.80};
    double threshold = 0.6;
    NMS nms = NMS();
    vector<int> index = nms.after_NMS(boxes,scores,threshold);
    for(int i =0;i<index.size();i++){
        cout<<index[i]<<" ";
    }
    //system("pause");
    return 0;
}
